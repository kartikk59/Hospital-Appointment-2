from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    residence = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    APPOINTMENT_STATUS = [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_no = models.CharField(max_length=10, unique=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    department = models.CharField(max_length=100)
    doctor = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment_no} - {self.patient.name}"

    class Meta:
        ordering = ['-appointment_date', '-appointment_time'] 