from .models import Country
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# Validation Sections
def alphaAllow(name,field_name):
    if not name.isalpha():
        raise ValidationError(f'{field_name} must contain only characters')
    
def alphaAllow(name,field_name):
    if not name.isalpha():
        raise ValidationError(f'{field_name} must contain only characters')
    
def validate_name_length(name,field_name):
    words = name.split()
    max_characters = 30 
    if len(name) > max_characters:
        raise ValidationError(f'Name must have at most {max_characters} characters.')
    
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
    
def Validate_img_extension(value):
   if value is not None and hasattr(value, 'name'): 
        ext = value.name.split('.')[-1]
        allowed_extension = ['jpg','jpeg','png','gif','svg']
        if ext.lower() not in allowed_extension:
            raise ValidationError(f'Only JPG, JPEG, PNG, or GIF files are allowed.')
   else:
       raise ValidationError(f'Please Add Images')
# End Validation Sections

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def country_page(request):
    country = Country.objects.all()
    paginator = Paginator(country, 8) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'cms/country.html',{'page_obj':page_obj})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def add_country_page(request):
        if request.method == 'POST':
            name = request.POST.get('name')
            image = request.FILES.get('image')

            try:
                Required(name,'name')
                alphaAllow(name,'name')
                validate_name_length(name,'name')
                Validate_img_extension(image)
                country = Country(name=name,image=image)
                country.save()
                messages.success(request, "Country added successfully")
                return redirect('country')
            except ValidationError as e:
                messages.error(request,str(e))

        return render(request, 'cms/country_add.html')

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def update_country_page(request, pk):
    try:
        country = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        country = None

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        try:
            if country:
                if image:
                    Validate_img_extension(image)
                    old_image_path = country.image.path  # Store the old image path before updating
                    country.image = image

                Required(name, 'name')
                alphaAllow(name, 'name')
                validate_name_length(name, 'name')

                country.name = name
                country.save()

                if image and os.path.exists(old_image_path):
                    os.remove(old_image_path)

                messages.info(request, "Country update successfully")
                return redirect('country')
            
            else:
                Validate_img_extension(image)
                Required(name, 'name')
                alphaAllow(name, 'name')
                validate_name_length(name, 'name')

                country = Country.objects.create(pk=pk, name=name, image=image)
                country.save()
                messages.info(request, "Country update successfully")
                return redirect('country')

        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'cms/country_update.html', {'country': country})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def delete_country_page(request,pk):
    contact = Country.objects.get(pk=pk)
    contact.delete()
    messages.warning(request, "Country deleted successfully")
    return redirect('country')