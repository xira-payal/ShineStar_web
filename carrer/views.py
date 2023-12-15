import os
from django.shortcuts import render , redirect
from .models import Carrer
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
    
def validate_file_extension(value):
    ext = value.name.split('.')[-1]
    allowed_extension = ['pdf','doc','docx','odt','txt']
    if ext.lower() not in allowed_extension:
         raise ValidationError(f'Only PDF, DOC, DOCX, TXT, or ODT files are allowed.')

def validate_phone_number(value):
    phone_number = str(value)  # Convert the value to a string for length check
    min_length = 5
    max_length = 20

    if not phone_number.isdigit() or not (min_length <= len(phone_number) <= max_length):
        raise ValidationError('Phone number must be a numeric value with length between 5 and 10 digits.')
# End Validation Sections

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def carrer_page(request):
    carrer = Carrer.objects.all()
    paginator = Paginator(carrer, 8) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'cms/carrer.html',{'page_obj':page_obj})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def add_carrer_page(request):
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
        try:
            Required(firstname,'firstname')
            Required(lastname,'lastname')
            Required(email,'email')
            validate_phone_number(phone),'phone'
            validate_file_extension(files)
            carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
            carrer.save()
            messages.success(request, "Career added successfully")
            return redirect('carrer')
        except ValidationError as e:
            messages.error(request,str(e))
    return render(request,'cms/carrer_add.html')

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def update_carrer_page(request, pk):
    if pk == pk:
        try:
            carrer = Carrer.objects.get(pk=pk)
        except Carrer.DoesNotExist:
            carrer = None

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

            if carrer:
                if files:
                    if carrer.files:
                        os.remove(carrer.files.path)
                        carrer.files = files

                carrer.firstname = firstname
                carrer.lastname = lastname
                carrer.email = email
                carrer.phone = phone
                carrer.address = address
                carrer.message = message
                carrer.education = education
                carrer.experiance = experiance
                carrer.save()
                messages.info(request, "Career Updated successfully")
                return redirect('carrer')
            else:
                carrer = Carrer(pk=pk,firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
                carrer.save()
                messages.info(request, "Career Updated successfully")
                return redirect('carrer')
    else:
        pass

    return render(request, 'cms/carrer_update.html', {'carrer': carrer})


@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def delete_carrer_page(request,pk):
    carrer = Carrer.objects.get(pk=pk)
    carrer.delete()
    messages.warning(request, "Career deleted successfully")
    return redirect('carrer')

@login_required(login_url='front-login')
def carrer_pages(request):
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
        try:
            carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
            carrer.save()
            messages.success(request, 'Your Career has Been Submited.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
     return render(request,'web/career.html')


@login_required(login_url='front-login')
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
        try:
            carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
            carrer.save()
            messages.success(request, 'Job has Been Apply.')
            return redirect('front-apply')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')        
    else:
        pass
    return render(request,'web/apply-opening.html')
