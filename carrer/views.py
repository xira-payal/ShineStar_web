from django.shortcuts import render , redirect
from .models import Carrer
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
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
# End Validation Sections

def carrer_page(request):
    carrer = Carrer.objects.all()
    paginator = Paginator(carrer, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'backend-template/carrer.html',{'page_obj':page_obj})

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
            validate_file_extension(files)
            carrer = Carrer(firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
            carrer.save()
            return redirect('carrer')
        except ValidationError as e:
            messages.error(request,str(e))
    return render(request,'backend-template/carrer_add.html')

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
                return redirect('carrer')
            else:
                carrer = Carrer(pk=pk,firstname=firstname,lastname=lastname,email=email,phone=phone,address=address,message=message,education=education,experiance=experiance,files=files)
                carrer.save()
                return redirect('carrer')
    else:
        pass

    return render(request, 'backend-template/carrer_update.html', {'carrer': carrer})


def delete_carrer_page(request,pk):
    carrer = Carrer.objects.get(pk=pk)
    carrer.delete()
    return redirect('carrer')

def go_back(request):
     previous_url = request.META.get('HTTP_REFERER')
     return redirect(previous_url,'blog')