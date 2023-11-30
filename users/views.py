from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Required(username,'username')
            Required(password,'password')

            user = authenticate(request, username=username, password=password)
            print(f'user {user.is_superuser}')
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('contact')
            else:
                messages.error(request, 'Only Super Admins can log in.')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'cms/login.html')

def logoutPage(request):
    logout(request)
    return redirect('admin_home')

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def homePage(request):
    username = request.user.username
    context = { 'username' : username }
    return render(request, 'cms/contact.html',context)