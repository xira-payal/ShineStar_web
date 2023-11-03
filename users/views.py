from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages

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

            if user is not None:
                login(request, user)
                return redirect('home')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'backend-template/login.html')

@login_required(login_url='/login')
def homePage(request):
    username = request.user.username
    context = { 'username' : username }
    return render(request, 'backend-template/contact.html',context)

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        try:
            Required(username,'username')
            Required(email,'emil')
            Required(password,'password')
            Required(confirm_password,'confirm_password')
            if password == confirm_password:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
            else:
               messages.error(request, 'Password Not Match')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'backend-template/register.html')

def forgotPassword(request):
    if request.method == 'POST':
      username = request.POST.get('username')
      email = request.POST.get('email')
      password = request.POST.get('password')
    return render(request, 'backend-template/forgotPassword.html')

def logoutPage(request):
    logout(request)
    return redirect('home')

