from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .forms import PatientCreationForm,UserLoginForm,FormHospital,ReceptionistCreationForm,DoctorCreationForm,AppointmentForm
from django.db import transaction
from django.db.utils import InternalError,DatabaseError
from .models import Patients,Receptionist,Doctor,Hospital,Appointment
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Group,User
from .decorators import isAuthenticated
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail


def Home(request):
         address = 'home.html'
         return render(request,address)

def UserRegister(request):
        if request.method == 'POST':
                form = PatientCreationForm(request.POST)
                if form.is_valid():   
                       try:
                           with transaction.atomic():
                                  Address = form.cleaned_data.get('address')
                                  phone_no = form.cleaned_data.get('phone_no')
                                  Date_of_birth = form.cleaned_data.get('date_of_birth')
                                  group = Group.objects.filter(name='Patients').first()
                                  user = form.save()
                                  user.groups.add(group)
                                  print(Address)
                                  patients_profile = Patients.objects.create(user_id=user,phone=phone_no,address=Address,date_of_birth=Date_of_birth)
                                  return redirect('UserLogin')
                       except (Exception,InternalError,DatabaseError) as e:
                              return HttpResponse(e)     


        else:
                form =  PatientCreationForm()

        address = 'Users/Patients/register.html'          
        context = {'form':form}
        return render(request,address,context)


def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@isAuthenticated
def UserLogin(request):
        address = 'Users/Patients/login.html'
        if request.method == 'POST':    
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request,username=username,password=password)
                print(user)
                print(username) 
                if user is not None:
                        print(user.groups.filter(name='Patients').exists())

                        if is_in_group(user,'Patients'):
                                print('UserLogin Page')
                                login(request,user)
                                return redirect('Home')
                        elif is_in_group(user,'Doctor'):
                                login(request,user)
                                return redirect('DoctorAdmin')
                        elif is_in_group(user,'Admin'):
                                login(request,user)
                                return redirect('Admin')
                        elif is_in_group(user,'Reciptionist'):
                                login(request,user)
                                return redirect('ReciptionistAdmin')
                        else:
                               print('Your account is not assigned to any role.')
                               return redirect('UserLogin')


                else:
                        messages.info(request,'You Entered Wrong Username and Password')
                        return redirect('UserLogin')       
        form = UserLoginForm() 
        context = {'form' : form}
        return render(request,address,context)    

@login_required
@isAuthenticated
def AdminDashboard(request):
       address = 'Users/Admin/Dashboard.html'
       return render(request,address)

def UserLogOut(request):
        logout(request)
        return render(request,'home.html')

@login_required
def HospitalForms(request):
       form = FormHospital()
       if request.method == 'POST':
              form = FormHospital(request.POST)
              if form.is_valid():
                     try:
                           with transaction.atomic():
                                  name = form.cleaned_data.get('name')
                                  address = form.cleaned_data.get('address')
                                  phone = form.cleaned_data.get('phone')
                                  email = form.cleaned_data.get('email')
                                  print(f"{name} {address} {phone} {email}")
                                  user = form.save()
                                  return redirect('Admin')
                     except (Exception,InternalError,DatabaseError) as e:
                              return HttpResponse(e)    
                     
                     
       return render(request,'Users/Admin/forms/hospitalForm.html',{'form':form})       
       
@login_required
def ReciptForms(request):
       if request.method == 'POST':
                form = ReceptionistCreationForm(request.POST)
                if form.is_valid(): 
                       try:
                           with transaction.atomic():
                                 hospital = form.cleaned_data['hospital']
                                 phone_no = form.cleaned_data['phone_no']
                                 group = Group.objects.get(name='Reciptionist')  # use get, not filter
                                 user = form.save()
                                 user.groups.add(group)
                                 Receptionist.objects.create(user=user, hospital=hospital, phone=phone_no)
                                 return redirect('Admin')
                       except (Exception,InternalError,DatabaseError) as e:
                              return HttpResponse(e)     
                return render(request, 'Users/Admin/forms/ReciptionistForm.html', {'form': form})


       else:
                form  = ReceptionistCreationForm()
                return render(request,'Users/Admin/forms/ReciptionistForm.html',{'form':form})


@login_required
def ReciptionistDashboard(request):
       address = 'Users/Reciptions/Dashboard.html'
       return render(request,address)

@login_required
def DoctorForms(request):
    receptionist = Receptionist.objects.get(user=request.user)
    hospital = receptionist.hospital

    if request.method == "POST":
        form = DoctorCreationForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                 
                    user = form.save()

                  
                    Doctor.objects.create(
                        user=user,
                        hospital=hospital,
                        added_by=receptionist,
                        speciality=form.cleaned_data['speciality'],
                        phone=form.cleaned_data['phone'],
                        image_url=form.cleaned_data['image_url'],
                        available_from=form.cleaned_data['available_from'],
                        available_to=form.cleaned_data['available_to'],
                    )

                return redirect('ReciptionistAdmin')

            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")

    else:
        form = DoctorCreationForm()

    return render(request, "Users\Doctors\dashboard.html", {"form": form})

@login_required
def DoctorList(request):
    # Get the logged-in receptionist
    recip = Receptionist.objects.get(user=request.user)

    # Fetch only doctors from that receptionist’s hospital
    doctors = Doctor.objects.filter(hospital=recip.hospital)

    return render(request, 'Users\Doctors\DoctorList.html', {'doctors': doctors})

@login_required
def DeleteDoctor(request, doctor_id):
    recip = Receptionist.objects.get(user=request.user)

   
    doctor = get_object_or_404(Doctor, id=doctor_id, hospital=recip.hospital)

    doctor.delete()
    messages.success(request, "Doctor removed successfully.")
    return redirect('DoctorList')

# ---------------------- LIST VIEWS -------------------------

def ViewHospitals(request):
    hospitals = Hospital.objects.all()
    return render(request, "Users/Admin/view_hospitals.html", {"hospitals": hospitals})

def ViewReciptionists(request):
    receptionists = Receptionist.objects.select_related("user", "hospital").all()
    return render(request, "Users/Admin/view_receptionists.html", {"receptionists": receptionists})

def ViewUsers(request):
    users = User.objects.all()
    return render(request, "Users/Admin/view_users.html", {"users": users})

# ---------------------- DELETE VIEWS -------------------------

def DeleteHospital(request, id):
    Hospital.objects.filter(id=id).delete()
    return redirect("ViewHospitals")

def DeleteReceptionist(request, id):
    Receptionist.objects.filter(id=id).delete()
    return redirect("ViewReciptionists")

def DeleteUser(request, id):
    User.objects.filter(id=id).delete()
    return redirect("ViewUsers")



# ---------------------- VIEW DOCTORS ADDED BY A RECEPTIONIST -------------------------

def ViewDoctorsByReceptionist(request, rid):
    receptionist = get_object_or_404(Receptionist, id=rid)
    doctors = Doctor.objects.filter(added_by=receptionist)
    return render(request, "Users/Admin/view_doctors_by_receptionist.html", {
        "receptionist": receptionist,
        "doctors": doctors
    })

def DeleteDoctor(request, id):
    Doctor.objects.filter(id=id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'ViewReciptionists'))

@login_required
def PatientDashboard(request):
    return render(request, "Users/Patients/PatientDashboard.html")


@login_required
def PatientViewInfo(request):
    patient = Patients.objects.get(user_id=request.user)
    return render(request, "Users/Patients/PatientViewInfo.html", {"patient": patient})

@login_required
def EditPatientInfo(request):
    patient = Patients.objects.get(user_id=request.user)

    if request.method == "POST":
        # Update USER model fields
        request.user.username = request.POST.get("username")
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update PATIENT model fields
        patient.phone = request.POST.get("phone")
        patient.address = request.POST.get("address")
        patient.date_of_birth = request.POST.get("date_of_birth")
        patient.save()

        messages.success(request, "Information updated successfully!")
        return redirect("PatientViewInfo")

    return render(request, "Users/Patients/EditPatientInfo.html", {"patient": patient})


def HospitalsList(request):
    hospitals = Hospital.objects.all()
    return render(request, "Users/hospitals_list.html", {"hospitals": hospitals})

def ViewHospitalDoctors(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    doctors = Doctor.objects.filter(hospital=hospital)
    return render(request, "Users/hospital_doctors.html", {
        "hospital": hospital,
        "doctors": doctors
    })

@login_required
def BookAppointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    hospital = doctor.hospital
    patient = get_object_or_404(Patients, user_id=request.user)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.hospital = hospital
            appointment.save()

            return redirect("AppointmentSuccess")
    else:
        form = AppointmentForm()

    return render(request, "Users/Patients/book_appointment.html", {
        "form": form,
        "doctor": doctor,
        "hospital": hospital,
        "patient": patient,
    })

def AppointmentSuccess(request):
    return render(request, "Users/Patients/appointment_success.html")

def PatientAppointments(request):
    patient = Patients.objects.get(user_id=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by("-appointment_date", "-appointment_time")

    return render(request, "Users/Patients/patient_appointments.html", {
        "appointments": appointments
    })


@login_required
def CancelAppointment(request, appointment_id):
    # Get the logged-in patient
    patient = get_object_or_404(Patients, user_id=request.user)

    # Fetch appointment that belongs to THIS patient
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    appointment.delete()
    
    return redirect("PatientAppointments")

@login_required
def ReceptionistAppointments(request):
    receptionist = request.user.receptionist  # current logged-in receptionist
    hospital = receptionist.hospital          # hospital they belong to

    appointments = Appointment.objects.filter(hospital=hospital).order_by("-created_at")

    return render(request, "Users/Reciptions/receptionist_appointments.html", {
        "appointments": appointments,
        "hospital": hospital
    })

@login_required
def HospitalAppointments(request, id):
    hospital = Hospital.objects.get(id=id)
    appointments = Appointment.objects.filter(hospital=hospital)

    return render(request, "Users/Admin/HospitalAppointments.html", {
        "hospital": hospital,
        "appointments": appointments
    })

@login_required
@login_required
def confirm_appointment(request, id):
    ap = Appointment.objects.get(id=id)
    ap.status = "Confirmed"
    ap.save()

    patient = ap.patient           # Patients model object
    user = patient.user_id         # Django User object

    # Correct Email
    email_to = user.email

    # Doctor & Hospital details
    doctor = ap.doctor
    hospital = doctor.hospital     # The hospital related to doctor

    # Email message
    subject = "Your Appointment is Confirmed"
    message = f"""
Hello {user.first_name},

Your appointment has been confirmed.

Hospital: {hospital.name}
Doctor: {doctor.user.first_name} {doctor.user.last_name}
Speciality: {doctor.speciality}
Date: {ap.appointment_date}
Time: {ap.appointment_time}

Thank you,
{hospital.name} Team
"""

    send_mail(
        subject,
        message,
        "yoga&ayurvediccare@gmail.com",
        [email_to],
        fail_silently=False,
    )

    return redirect("ReceptionistAppointments")



@login_required
def reject_appointment(request, id):
    ap = Appointment.objects.get(id=id)
    ap.status = "Rejected"
    ap.save()
    doctor = ap.doctor
    hospital = doctor.hospital
    patient = ap.patient
    user = patient.user_id

    email_to = user.email

    subject = "Your Appointment Has Been Rejected"
    message = f"""
Hello {user.first_name},

We are sorry to inform you that your appointment has been rejected.

Hospital: {hospital.name}
Doctor: {ap.doctor.user.first_name} {ap.doctor.user.last_name}
Speciality: {ap.doctor.speciality}
Date: {ap.appointment_date}
Time: {ap.appointment_time}

Please try booking again or choose another doctor.

Thank you,
{hospital.name} Team
"""

    send_mail(
        subject,
        message,
        "yoga&ayurvediccare@gmail.com",
        [email_to],
        fail_silently=False,
    )

    return redirect("ReceptionistAppointments")

