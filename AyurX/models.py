from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Appointment(models.Model):
    patient = models.ForeignKey("Patients", on_delete=models.CASCADE)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE)
    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    symptoms = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment - {self.patient.user_id.first_name} with Dr.{self.doctor.user.first_name}"


class Patients(models.Model):
         user_id = models.OneToOneField(User,on_delete=models.CASCADE)
         phone = models.CharField(max_length=15)
         address = models.TextField(blank=True,null=True)
         date_of_birth = models.DateField(blank=True,null=True)

         def __str__(self):
                 return f"{self.user_id.first_name}"
   
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    image_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="receptionists")
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receptionist: {self.user.username} ({self.hospital.name})"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="doctors")
    added_by = models.ForeignKey(Receptionist, on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    image_url = models.TextField(blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()


    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.speciality})"
