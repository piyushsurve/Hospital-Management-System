from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
import re
from AyurX.models import Hospital,Doctor,Receptionist,Appointment

class FormHospital(forms.ModelForm):
       class Meta:
              model = Hospital
              fields = '__all__'
              widgets = {
                         'name' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),
                           'address' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),
                             'phone' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),
                              'email' : forms.EmailInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),
                              'image_url' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),
              }

       def clean_phone(self):
                  phone = self.cleaned_data.get('phone')
                  pattern = r'^\+91\d{10}$'
                  if not re.fullmatch(pattern, phone):
                           raise forms.ValidationError("Phone number must start with +91 and be followed by 10 digits.")
                  return phone


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 w-full border-4 border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
            })

    class Meta:
           model = User
           field =  '__all__'


class ReceptionistCreationForm(UserCreationForm):
       phone_no = forms.CharField(max_length=15,required=True,widget=forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}))

       hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
            }
        ),
        label="Select Hospital"
    )

       class Meta:
                 model  = User
                 fields = ['username','first_name','last_name','email','password1','password2']
                 widgets = {
                         'username' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'first_name':forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                          'last_name':forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'email' : forms.EmailInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'password1': forms.PasswordInput(attrs={
                        'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
                        }),
                        'password2': forms.PasswordInput(attrs={
                        'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
                        }),

                 }
       def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field_name in self.fields:
                        self.fields[field_name].widget.attrs['class'] = (
            'mt-1 w-full rounded-md border-2 border-gray-500 p-2 '
            'focus:ring-blue-500 focus:border-blue-500'
        )


       def clean_phone_no(self):
                   phone = self.cleaned_data.get('phone_no')
                   pattern = r'^\+91\d{10}$'
                   if not re.fullmatch(pattern, phone):
                           raise forms.ValidationError("Phone number must start with +91 and be followed by 10 digits.")
                   return phone


class PatientCreationForm(UserCreationForm):
         phone_no = forms.CharField(max_length=15,required=True,widget=forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}))
         address = forms.CharField(widget=forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}))
         date_of_birth = forms.DateField(required=True,widget=forms.DateInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500','type':'date'}))
         class Meta:
                 model  = User
                 fields = ['username','first_name','last_name','email','password1','password2']
                 widgets = {
                         'username' : forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'first_name':forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                          'last_name':forms.TextInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'email' : forms.EmailInput(attrs={'class':'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'}),

                         'password1': forms.PasswordInput(attrs={
                        'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
                        }),
                        'password2': forms.PasswordInput(attrs={
                        'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
                        }),

                 }

         def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field_name in self.fields:
                        self.fields[field_name].widget.attrs.update({
                                'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
                        })       

         def clean_phone_no(self):
                  phone = self.cleaned_data.get('phone_no')
                  pattern = r'^\+91\d{10}$'
                  if not re.fullmatch(pattern, phone):
                           raise forms.ValidationError("Phone number must start with +91 and be followed by 10 digits.")
                  return phone


class DoctorCreationForm(UserCreationForm):
    speciality = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    image_url = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    available_from = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    available_to = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'mt-1 w-full rounded-md border-2 border-gray-500 p-2 focus:ring-blue-500 focus:border-blue-500'
            })

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^\+91\d{10}$'
        if not re.fullmatch(pattern, phone):
            raise forms.ValidationError("Phone number must start with +91 and be followed by 10 digits.")
        return phone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_date", "appointment_time", "symptoms"]

        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),
            "symptoms": forms.Textarea(attrs={"rows": 3}),
        }
    
