
from django.shortcuts import redirect,render
from django.urls import resolve
from django.http import HttpResponse


def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def isAuthenticated(view_func):
         def wrapper_func(request,*args,**kwargs):
                 if request.user.is_authenticated:
                        current_path = resolve(request.path).url_name
                        if is_in_group(request.user,'Patients') and current_path != 'Home':
                               return redirect('Home')
                        elif is_in_group(request.user,'Doctor') and current_path != '#':
                                return redirect('DoctorAdmin')
                        elif is_in_group(request.user,'Reciptionist') and current_path != 'ReciptionistAdmin':
                                return redirect('ReciptionistAdmin')
                        elif is_in_group(request.user,'Admin') and current_path != 'Admin':
                                return redirect('Admin')
                        return view_func(request, *args, **kwargs)
                 else:
                        return view_func(request, *args, **kwargs)
                 
         return wrapper_func
                        
                         