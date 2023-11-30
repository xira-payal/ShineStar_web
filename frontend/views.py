from django.shortcuts import render , redirect
from contact.models import Contact
from carrer.models import Carrer
from country.models import Country
from opening.models import Opening
from blog.models import Blogs
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import activate
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections

def register_page(request):
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
                return redirect('front-login')
            else:
               messages.error(request, 'Password Not Match')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request,'web/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Required(username, 'username')
            Required(password, 'password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('front-apply')
            else:
                raise ValidationError('Invalid username or password')

        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'web/login.html')

def index_page(request):
    positions = Opening.objects.all()
    country = Country.objects.all()
    blogs = Blogs.objects.all()
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        positions = positions.filter(location=selected_country_id)
    return render(request,'web/index.html',{'country':country,'positions':positions,'blogs':blogs})

def about_page(request):
    return render(request,'web/about-us.html')

def logout_page(request):
    logout(request)
    return redirect('front-home')

def about_page(request):
    return render(request,'web/about-us.html')