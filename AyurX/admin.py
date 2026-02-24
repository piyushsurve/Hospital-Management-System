from django.contrib import admin
from .models import Patients
from django.contrib.auth.models import Group

@admin.register(Patients)
class AdminPatients(admin.ModelAdmin):
    list_display = ['get_firstName','get_lastName','get_username','get_password', 'get_email', 'phone', 'address', 'date_of_birth','get_groups']

    def get_username(self, obj):
        return obj.user_id.username
    get_username.short_description = 'Username'

    def get_groups(self, obj):
        groups = obj.user_id.groups.all()
        if groups.exists():
           return ", ".join([g.name for g in groups])
        return "-"
    get_groups.short_description = 'Group'


    def get_email(self, obj):
        return obj.user_id.email
    get_email.short_description = 'Email'

    def get_firstName(self, obj):
        return obj.user_id.first_name
    get_firstName.short_description = 'First Name'

    def get_lastName(self, obj):
        return obj.user_id.last_name
    get_lastName.short_description = 'Last Name'

    def get_password(self, obj):
        return obj.user_id.password
    get_password.short_description = 'Password'

