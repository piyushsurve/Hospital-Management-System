from django.urls import path
from AyurX import views

urlpatterns = [
    path('',views.Home,name='Home'),
    path('UserRegister',views.UserRegister,name='UserRegister'),
    path('UserLogin',views.UserLogin,name='UserLogin'),
    path('UserLogOut',views.UserLogOut,name='UserLogOut'),
    path('Admin',views.AdminDashboard,name='Admin'),
    path('ReciptionistAdmin',views.ReciptionistDashboard,name='ReciptionistAdmin'),
    path('Admin/Hospital-forms', views.HospitalForms, name='HospitalForms'),
    path('Admin/Reciptionist-forms', views.ReciptForms, name='ReciptionForms'),
    path('ReciptionistAdmin/Doctor-forms', views.DoctorForms, name='DoctorForms'),
    path('ReciptionistAdmin/Doctors', views.DoctorList, name='DoctorList'),
    path('ReciptionistAdmin/DeleteDoctor/<int:doctor_id>', views.DeleteDoctor, name='DeleteDoctor'),
    path('Admin/Hospitals', views.ViewHospitals, name='ViewHospitals'),
    path('Admin/Receptionists', views.ViewReciptionists, name='ViewReciptionists'),
    path('Admin/Users', views.ViewUsers, name='ViewUsers'),
    path('Admin/Delete-Hospital/<int:id>', views.DeleteHospital, name='DeleteHospital'),
    path('Admin/Delete-Receptionist/<int:id>', views.DeleteReceptionist, name='DeleteReceptionist'),
    path('Admin/Delete-User/<int:id>', views.DeleteUser, name='DeleteUser'),
    path('Admin/Doctors/<int:rid>', views.ViewDoctorsByReceptionist, name='ViewDoctorsByReceptionist'),
    path('Admin/Delete-Doctor/<int:id>', views.DeleteDoctor, name='DeleteDoctor'),
    path("patient/dashboard/", views.PatientDashboard, name="PatientDashboard"),
    path("patient/view-info/", views.PatientViewInfo, name="PatientViewInfo"),
    path("patient/edit-info/", views.EditPatientInfo, name="EditPatientInfo"),
    path("hospitals/", views.HospitalsList, name="HospitalsList"),
    path("hospital/<int:hospital_id>/doctors/", views.ViewHospitalDoctors, name="ViewHospitalDoctors"),
    path("appointment/book/<int:doctor_id>/", views.BookAppointment, name="BookAppointment"),
    path("appointment/success/", views.AppointmentSuccess, name="AppointmentSuccess"),
    path("patient/appointments/", views.PatientAppointments, name="PatientAppointments"),
    path("appointments/cancel/<int:appointment_id>/", views.CancelAppointment, name="CancelAppointments"),
    path("receptionist/appointments/", views.ReceptionistAppointments, name="ReceptionistAppointments"),
    path("hospital/<int:id>/appointments/", views.HospitalAppointments, name="HospitalAppointments"),
    path('appointment/<int:id>/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('appointment/<int:id>/reject/', views.reject_appointment, name='reject_appointment'),





]








