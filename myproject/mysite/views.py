import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Patient, Appointment
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


# Flask API base URL
API_BASE_URL = 'http://localhost:5000/api'

DEPARTMENTS = {
    'cardiology': {
        'name': 'Cardiology',
        'slug': 'cardiology',
        'icon': 'fas fa-heart',
        'description': 'Our Cardiology department provides comprehensive care for all types of cardiovascular conditions. Equipped with state-of-the-art technology and staffed by experienced cardiologists.',
        'doctors': [
            {
                'id': 1,
                'name': 'Dr. John Smith',
                'specialization': 'Senior Cardiologist',
                'qualifications': 'MBBS, MD, DM (Cardiology)',
                'image': None,
                'experience': '15 years'
            },
            {
                'id': 2,
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Interventional Cardiologist',
                'qualifications': 'MBBS, DNB (Cardiology)',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 3,
                'name': 'Dr. Michael Chen',
                'specialization': 'Pediatric Cardiologist',
                'qualifications': 'MBBS, MD, Fellowship in Pediatric Cardiology',
                'image': None,
                'experience': '10 years'
            },
            {
                'id': 4,
                'name': 'Dr. Emily Brown',
                'specialization': 'Clinical Cardiologist',
                'qualifications': 'MBBS, MD (Cardiology)',
                'image': None,
                'experience': '8 years'
            }
        ]
    },
    'orthopedics': {
        'name': 'Orthopedics',
        'slug': 'orthopedics',
        'icon': 'fas fa-bone',
        'description': 'Our Orthopedics department specializes in the treatment of musculoskeletal conditions, offering both surgical and non-surgical solutions for bone and joint problems.',
        'doctors': [
            {
                'id': 5,
                'name': 'Dr. Robert Wilson',
                'specialization': 'Joint Replacement Surgeon',
                'qualifications': 'MBBS, MS (Ortho), Fellowship in Joint Replacement',
                'image': None,
                'experience': '18 years'
            },
            {
                'id': 6,
                'name': 'Dr. Lisa Anderson',
                'specialization': 'Spine Surgeon',
                'qualifications': 'MBBS, MS (Ortho), Fellowship in Spine Surgery',
                'image': None,
                'experience': '14 years'
            },
            {
                'id': 7,
                'name': 'Dr. David Lee',
                'specialization': 'Sports Medicine Specialist',
                'qualifications': 'MBBS, MS (Ortho), Sports Medicine',
                'image': None,
                'experience': '11 years'
            },
            {
                'id': 8,
                'name': 'Dr. Rachel Martinez',
                'specialization': 'Pediatric Orthopedist',
                'qualifications': 'MBBS, DNB (Ortho)',
                'image': None,
                'experience': '9 years'
            }
        ]
    },
    'dental': {
        'name': 'Dental Care',
        'slug': 'dental',
        'icon': 'fas fa-tooth',
        'description': 'Our Dental department offers comprehensive dental care services including preventive care, cosmetic dentistry, orthodontics, and oral surgery.',
        'doctors': [
            {
                'id': 9,
                'name': 'Dr. James Taylor',
                'specialization': 'Orthodontist',
                'qualifications': 'BDS, MDS (Orthodontics)',
                'image': None,
                'experience': '16 years'
            },
            {
                'id': 10,
                'name': 'Dr. Maria Garcia',
                'specialization': 'Oral Surgeon',
                'qualifications': 'BDS, MDS (Oral Surgery)',
                'image': None,
                'experience': '13 years'
            },
            {
                'id': 11,
                'name': 'Dr. Thomas White',
                'specialization': 'Cosmetic Dentist',
                'qualifications': 'BDS, Advanced Cosmetic Dentistry',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 12,
                'name': 'Dr. Sophie Clark',
                'specialization': 'Periodontist',
                'qualifications': 'BDS, MDS (Periodontics)',
                'image': None,
                'experience': '10 years'
            }
        ]
    },
    'neurology': {
        'name': 'Neurology',
        'slug': 'neurology',
        'icon': 'fas fa-brain',
        'description': 'Our Neurology department provides expert care for disorders of the nervous system, including brain, spinal cord, and peripheral nerve conditions.',
        'doctors': [
            {
                'id': 13,
                'name': 'Dr. William Parker',
                'specialization': 'Neurologist',
                'qualifications': 'MBBS, MD (Neurology), DM',
                'image': None,
                'experience': '20 years'
            },
            {
                'id': 14,
                'name': 'Dr. Jennifer Adams',
                'specialization': 'Pediatric Neurologist',
                'qualifications': 'MBBS, MD, Fellowship in Pediatric Neurology',
                'image': None,
                'experience': '15 years'
            },
            {
                'id': 15,
                'name': 'Dr. Richard Thompson',
                'specialization': 'Neurosurgeon',
                'qualifications': 'MBBS, MS, MCh (Neurosurgery)',
                'image': None,
                'experience': '17 years'
            },
            {
                'id': 16,
                'name': 'Dr. Amanda Lewis',
                'specialization': 'Neuro-psychiatrist',
                'qualifications': 'MBBS, MD (Psychiatry), Fellowship in Neuropsychiatry',
                'image': None,
                'experience': '12 years'
            }
        ]
    },
    'pediatrics': {
        'name': 'Pediatrics',
        'slug': 'pediatrics',
        'icon': 'fas fa-baby',
        'description': 'Our Pediatrics department provides comprehensive healthcare for children from birth through adolescence, focusing on their unique medical needs and development.',
        'doctors': [
            {
                'id': 17,
                'name': 'Dr. Sarah Williams',
                'specialization': 'General Pediatrician',
                'qualifications': 'MBBS, MD (Pediatrics)',
                'image': None,
                'experience': '15 years'
            },
            {
                'id': 18,
                'name': 'Dr. Michael Brown',
                'specialization': 'Pediatric Surgeon',
                'qualifications': 'MBBS, MS, MCh (Pediatric Surgery)',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 19,
                'name': 'Dr. Emily Davis',
                'specialization': 'Pediatric Endocrinologist',
                'qualifications': 'MBBS, MD, DM (Pediatric Endocrinology)',
                'image': None,
                'experience': '10 years'
            },
            {
                'id': 20,
                'name': 'Dr. James Wilson',
                'specialization': 'Pediatric Emergency Specialist',
                'qualifications': 'MBBS, MD, Fellowship in Pediatric Emergency',
                'image': None,
                'experience': '8 years'
            }
        ]
    },
    'ophthalmology': {
        'name': 'Ophthalmology',
        'slug': 'ophthalmology',
        'icon': 'fas fa-eye',
        'description': 'Our Ophthalmology department provides comprehensive eye care services, from routine check-ups to complex eye surgeries, using advanced technology and techniques.',
        'doctors': [
            {
                'id': 21,
                'name': 'Dr. Robert Chen',
                'specialization': 'Retina Specialist',
                'qualifications': 'MBBS, MS, Fellowship in Retina',
                'image': None,
                'experience': '16 years'
            },
            {
                'id': 22,
                'name': 'Dr. Lisa Anderson',
                'specialization': 'Cornea Specialist',
                'qualifications': 'MBBS, MS, Fellowship in Cornea',
                'image': None,
                'experience': '14 years'
            },
            {
                'id': 23,
                'name': 'Dr. David Miller',
                'specialization': 'Glaucoma Specialist',
                'qualifications': 'MBBS, MS, Fellowship in Glaucoma',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 24,
                'name': 'Dr. Rachel Taylor',
                'specialization': 'Pediatric Ophthalmologist',
                'qualifications': 'MBBS, MS, Fellowship in Pediatric Ophthalmology',
                'image': None,
                'experience': '10 years'
            }
        ]
    },
    'dermatology': {
        'name': 'Dermatology',
        'slug': 'dermatology',
        'icon': 'fas fa-allergies',
        'description': 'Our Dermatology department provides comprehensive care for skin, hair, and nail conditions, offering both medical and cosmetic treatments.',
        'doctors': [
            {
                'id': 25,
                'name': 'Dr. Sarah Martinez',
                'specialization': 'Medical Dermatologist',
                'qualifications': 'MBBS, MD (Dermatology)',
                'image': None,
                'experience': '15 years'
            },
            {
                'id': 26,
                'name': 'Dr. Michael Lee',
                'specialization': 'Cosmetic Dermatologist',
                'qualifications': 'MBBS, MD, Fellowship in Cosmetic Dermatology',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 27,
                'name': 'Dr. Emily Wilson',
                'specialization': 'Pediatric Dermatologist',
                'qualifications': 'MBBS, MD, Fellowship in Pediatric Dermatology',
                'image': None,
                'experience': '10 years'
            },
            {
                'id': 28,
                'name': 'Dr. James Anderson',
                'specialization': 'Surgical Dermatologist',
                'qualifications': 'MBBS, MD, Fellowship in Dermatosurgery',
                'image': None,
                'experience': '8 years'
            }
        ]
    },
    'ent': {
        'name': 'ENT',
        'slug': 'ent',
        'icon': 'fas fa-ear',
        'description': 'Our ENT (Ear, Nose, and Throat) department provides comprehensive care for disorders of the head and neck region, including hearing, balance, and voice disorders.',
        'doctors': [
            {
                'id': 29,
                'name': 'Dr. William Thompson',
                'specialization': 'ENT Surgeon',
                'qualifications': 'MBBS, MS (ENT), DNB',
                'image': None,
                'experience': '18 years'
            },
            {
                'id': 30,
                'name': 'Dr. Jennifer Davis',
                'specialization': 'Otologist',
                'qualifications': 'MBBS, MS, Fellowship in Otology',
                'image': None,
                'experience': '15 years'
            },
            {
                'id': 31,
                'name': 'Dr. Richard Wilson',
                'specialization': 'Rhinologist',
                'qualifications': 'MBBS, MS, Fellowship in Rhinology',
                'image': None,
                'experience': '12 years'
            },
            {
                'id': 32,
                'name': 'Dr. Amanda Brown',
                'specialization': 'Laryngologist',
                'qualifications': 'MBBS, MS, Fellowship in Laryngology',
                'image': None,
                'experience': '10 years'
            }
        ]
    }
}

def home(request):
    if request.user.is_authenticated:
        try:
            # Get JWT token from session
            jwt_token = request.session.get('jwt_token')
            if not jwt_token:
                messages.error(request, 'Please log in again')
                return redirect('login')

            print(f"JWT Token: {jwt_token}")  # Debug log

            # Call Flask API to get profile
            profile_response = requests.get(
                f'{API_BASE_URL}/profile',
                headers={'Authorization': f'Bearer {jwt_token}'}
            )
            print(f"Profile Response Status: {profile_response.status_code}")  # Debug log
            print(f"Profile Response Data: {profile_response.text}")  # Debug log

            # Call Flask API to get appointments
            appointments_response = requests.get(
                f'{API_BASE_URL}/appointments',
                headers={'Authorization': f'Bearer {jwt_token}'}
            )
            print(f"Appointments Response Status: {appointments_response.status_code}")  # Debug log
            print(f"Appointments Response Data: {appointments_response.text}")  # Debug log

            context = {
                'user': request.user,
                'appointments': []
            }

            if profile_response.status_code == 200:
                context['profile'] = profile_response.json()
            else:
                messages.warning(request, 'Could not fetch profile information')

            if appointments_response.status_code == 200:
                context['appointments'] = appointments_response.json()
            else:
                messages.warning(request, 'Could not fetch appointments')

            print(f"Context being passed to template: {context}")  # Debug log
            return render(request, 'home.html', context)
        except requests.RequestException as e:
            print(f"Request Exception: {str(e)}")  # Debug log
            messages.error(request, 'Unable to connect to the server')
            return render(request, 'home.html', {'user': request.user})
    else:
        return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def departments(request):
    return render(request, 'departments.html', {'departments': DEPARTMENTS.values()})

def department_detail(request, slug):
    department = DEPARTMENTS.get(slug)
    if not department:
        return redirect('departments')
    return render(request, 'department_detail.html', {'department': department})

def find_doctor(request):
    return render(request, 'find_doctor.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        try:
            # Get JWT token from session
            jwt_token = request.session.get('jwt_token')
            if not jwt_token:
                messages.error(request, 'Please log in again')
                return redirect('login')

            # Prepare appointment data
            appointment_data = {
                'department': request.POST.get('department'),
                'doctor': request.POST.get('doctor'),
                'date': request.POST.get('date'),
                'time': request.POST.get('time')
            }

            # Call Flask API to create appointment
            response = requests.post(
                f'{API_BASE_URL}/appointments',
                headers={'Authorization': f'Bearer {jwt_token}'},
                json=appointment_data
            )

            if response.status_code == 201:
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointments')
            else:
                error_message = response.json().get('message', 'Failed to book appointment')
                messages.error(request, error_message)
                return render(request, 'book_appointment.html', {
                    'departments': DEPARTMENTS.values(),
                    'form_data': request.POST
                })
        except requests.RequestException:
            messages.error(request, 'Unable to connect to the server')
            return render(request, 'book_appointment.html', {
                'departments': DEPARTMENTS.values(),
                'form_data': request.POST
            })

    return render(request, 'book_appointment.html', {'departments': DEPARTMENTS.values()})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')

@login_required
def appointments(request):
    try:
        # Get JWT token from session
        jwt_token = request.session.get('jwt_token')
        if not jwt_token:
            messages.error(request, 'Please log in again')
            return redirect('login')

        # Call Flask API to get appointments
        response = requests.get(
            f'{API_BASE_URL}/appointments',
            headers={'Authorization': f'Bearer {jwt_token}'}
        )

        if response.status_code == 200:
            appointments = response.json()
            return render(request, 'appointments.html', {'appointments': appointments})
        elif response.status_code == 401:
            messages.error(request, 'Session expired. Please log in again')
            return redirect('login')
        else:
            messages.error(request, 'Failed to fetch appointments')
            return render(request, 'appointments.html', {'appointments': []})
    except requests.RequestException:
        messages.error(request, 'Unable to connect to the server')
        return render(request, 'appointments.html', {'appointments': []})

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            # Call Flask API for registration
            response = requests.post(
                f'{API_BASE_URL}/register',
                json={
                    'name': name,
                    'email': email,
                    'password': password
                }
            )

            if response.status_code == 201:
                # Create Django user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name.split()[0],
                    last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
                )
                
                # Log in the user
                login(request, user)
                
                # Get JWT token by logging in
                login_response = requests.post(
                    f'{API_BASE_URL}/login',
                    json={
                        'email': email,
                        'password': password
                    }
                )
                
                if login_response.status_code == 200:
                    data = login_response.json()
                    request.session['jwt_token'] = data['token']
                
                messages.success(request, 'Registration successful!')
                return redirect('home')
            else:
                error_message = response.json().get('message', 'Registration failed')
                return render(request, 'register.html', {'error': error_message})
        except requests.RequestException:
            return render(request, 'register.html', {
                'error': 'Unable to connect to the server. Please try again later.'
            })

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        next_url = request.POST.get('next')

        try:
            # Call Flask API for authentication
            response = requests.post(
                f'{API_BASE_URL}/login',
                json={
                    'email': email,
                    'password': password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Create or update Django user
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'username': email,
                        'first_name': data['user']['name'].split()[0],
                        'last_name': ' '.join(data['user']['name'].split()[1:]) if len(data['user']['name'].split()) > 1 else ''
                    }
                )
                
                if created:
                    user.set_password(password)
                    user.save()
                
                # Log in the user
                login(request, user)
                
                # Store JWT token in session
                request.session['jwt_token'] = data['token']
                
                if not remember_me:
                    request.session.set_expiry(0)
                
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                return render(request, 'login.html', {
                    'error': response.json().get('message', 'Invalid email or password'),
                    'next': next_url
                })
        except requests.RequestException:
            return render(request, 'login.html', {
                'error': 'Unable to connect to the server. Please try again later.',
                'next': next_url
            })

    next_url = request.GET.get('next')
    return render(request, 'login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
                
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    return redirect('home')