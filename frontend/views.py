from django.shortcuts import render , redirect
from contact.models import Contact
from carrer.models import Carrer
from country.models import Country
from opening.models import Opening
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
import os
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
                return redirect('Front_login')
            else:
               messages.error(request, 'Password Not Match')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request,'frontend_template/register.html')

def login_page(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                Required(username,'username')
                Required(password,'password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('Front_apply')
            except ValidationError as e:
                messages.error(request, str(e))
        return render(request,'frontend_template/login.html')

def index_page(request):
    positions = Opening.objects.all()
    country = Country.objects.all()
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        positions = positions.filter(location=selected_country_id)
    return render(request,'frontend_template/index.html',{'country':country,'positions':positions})

def about_page(request):
    return render(request,'frontend_template/about-us.html')
    
def carrer_page(request):
     if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')
        education = request.POST.get('education')
        experiance = request.POST.get('experiance')
        files = request.FILES.get('files')
        carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
        carrer.save()
     return render(request,'frontend_template/career.html')

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name,email=email,phone=phone,message=message)
        contact.save()
    return render(request,'frontend_template/contact-us.html')

def opening_page(request):
    positions = Opening.objects.all()
    country = Country.objects.all()
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        positions = positions.filter(location=selected_country_id)
    return render(request,'frontend_template/current-openings.html',{'country':country,'positions':positions})

def apply_opening_page(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')
        education = request.POST.get('education')
        experiance = request.POST.get('experiance')
        files = request.FILES.get('files')
        carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
        carrer.save()
        return redirect('opening')
    else:
        pass
    return render(request,'frontend_template/apply-opening.html')

def logout_page(request):
    logout(request)
    return redirect('Front_Home')