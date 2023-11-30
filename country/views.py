from .models import Country
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required, user_passes_test
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
                Required(image,'image')
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
                messages.info(request, "Country update successfully")
                return redirect('country')
            else:
                country = Country.objects.create(pk=pk, name=name, image=image)
                country.save()
                messages.info(request, "Country update successfully")
                return redirect('country')
    else:
        pass
    return render(request, 'cms/country_update.html', {'country': country})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def delete_country_page(request,pk):
    contact = Country.objects.get(pk=pk)
    contact.delete()
    messages.warning(request, "Country deleted successfully")
    return redirect('country')