from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
# Update CORS configuration to allow requests from Django
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000", "http://127.0.0.1:8000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Secret key for JWT
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key

# Mock user database (replace with your actual user database)
users = {
    'user@example.com': {
        'password': 'password123',
        'name': 'Test User'
    }
}

# Mock appointments list
appointments = []

# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['email']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and password are required!'}), 400
    
    if email not in users or users[email]['password'] != password:
        return jsonify({'message': 'Invalid credentials!'}), 401
    
    # Create JWT token
    token = jwt.encode({
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'email': email,
            'name': users[email]['name']
        }
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    
    if not email or not password or not name:
        return jsonify({'message': 'All fields are required!'}), 400
    
    if email in users:
        return jsonify({'message': 'User already exists!'}), 400
    
    users[email] = {
        'password': password,
        'name': name
    }
    
    return jsonify({'message': 'User registered successfully!'}), 201

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'email': current_user,
        'name': users[current_user]['name']
    })

@app.route('/api/appointments', methods=['GET', 'POST'])
@token_required
def handle_appointments(current_user):
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['department', 'doctor', 'date', 'time']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        # Create new appointment
        new_appointment = {
            'id': len(appointments) + 1,
            'appointment_no': f'APT{str(len(appointments) + 1).zfill(3)}',
            'department': data['department'],
            'doctor': data['doctor'],
            'date': data['date'],
            'time': data['time'],
            'status': 'booked'
        }
        
        appointments.append(new_appointment)
        return jsonify(new_appointment), 201
    
    # GET method - return all appointments
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(debug=True, port=5000)