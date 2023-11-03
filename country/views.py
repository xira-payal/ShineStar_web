from .models import Country
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
    
def Validate_img_extension(value):
    ext = value.name.split('.')[-1]
    allowed_extension = ['jpg','jpeg','png','gif','svg']
    if ext.lower() not in allowed_extension:
         raise ValidationError(f'Only JPG, JPEG, PNG, or GIF files are allowed.')
# End Validation Sections

def country_page(request):
    country = Country.objects.all()
    paginator = Paginator(country, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'backend-template/country.html',{'page_obj':page_obj})

def add_country_page(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            image = request.FILES.get('image')

            try:
                Required(name,'name')
                Required(image,'image')
                Validate_img_extension(image)
                country = Country(name=name,image=image)
                country.save()
                return redirect('country')
            except ValidationError as e:
                messages.error(request,str(e))

        return render(request, 'backend-template/country_add.html')

def update_country_page(request, pk):
    if pk == pk:
        try:
            country = Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            country = None

        if request.method == 'POST':
            name = request.POST.get('name')
            image = request.FILES.get('image')

            if country:
                if image:
                    if country.image:
                        os.remove(country.image.path)
                    country.image = image
                country.name = name
                country.save()
                return redirect('country')
            else:
                country = Country.objects.create(pk=pk, name=name, image=image)
                country.save()
                return redirect('country')
    else:
        pass
    return render(request, 'backend-template/country_update.html', {'country': country})

def delete_country_page(request,pk):
    contact = Country.objects.get(pk=pk)
    contact.delete()
    return redirect('country')