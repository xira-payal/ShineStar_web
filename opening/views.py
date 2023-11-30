from django.shortcuts import render , redirect
from django.http import HttpResponseServerError
from .models import Opening
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Country 
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def opening_page(request):
    opening = Opening.objects.all()
    paginator = Paginator(opening, 8) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'cms/opening.html',{'page_obj':page_obj})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def add_opening_page(request):
    if request.method == 'POST':
        position = request.POST.get('position')
        company = request.POST.get('company')
        vaccancy = request.POST.get('vaccancy')
        salary = request.POST.get('salary')
        salaryEnd = request.POST.get('salaryEnd')
        description = request.POST.get('description')
        status = request.POST.get('status')
        location = request.POST.get('location') 
        if status == 'off':
            status = False
        else:
            status = True 

        try:
            Required(position, 'position')
            Required(company, 'company')
            Required(vaccancy, 'vaccancy')
            Required(salary, 'salary')
            Required(salaryEnd, 'salaryEnd')
            Required(description, 'description')
            location = Country.objects.get(pk=location)
            opening = Opening(position=position, company=company, vaccancy=vaccancy, salary=salary, salaryEnd=salaryEnd, description=description, location=location ,status=status)
            opening.save()
            messages.success(request, "Current Opening added successfully")

            return redirect('opening')
        except ValidationError as e:
            messages.error(request, str(e))
    
    countries = Country.objects.all()
    return render(request, 'cms/opening_add.html',{'countries':countries})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def update_opening_page(request, pk):
    try:
        opening = Opening.objects.get(pk=pk)
    except Opening.DoesNotExist:
        opening = None

    if request.method == 'POST':
        position = request.POST.get('position')
        company = request.POST.get('company')
        vaccancy = request.POST.get('vaccancy')
        salary = request.POST.get('salary')
        salaryEnd = request.POST.get('salaryEnd')
        location = request.POST.get('location') 
        description = request.POST.get('description')
        status = request.POST.get('status')

        status = (status == 'on')

        if opening:
            opening.position = position
            opening.company = company
            opening.vaccancy = vaccancy
            opening.salary = salary
            opening.salaryEnd = salaryEnd

            location = Country.objects.get(pk=location)
            opening.location = location

            opening.description = description
            opening.status = status

            try:
                opening.save()
                messages.info(request, "Current Opening Update successfully")
            except Exception as e:
                return HttpResponseServerError("An error occurred while saving the data.")

            return redirect('opening')
    else:
        countries = Country.objects.all()
        return render(request, 'cms/opening_update.html', {'opening': opening, 'countries': countries})

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def delete_opening_page(request,pk):
    opening = Opening.objects.get(pk=pk)
    opening.delete()
    messages.warning(request, "Current Opening Delete successfully")
    return redirect('opening')

def opening_pages(request):
    positions = Opening.objects.all()
    country = Country.objects.all()
    selected_country_id = request.GET.get('country')
    if selected_country_id:
        positions = positions.filter(location=selected_country_id)
    return render(request,'web/current-openings.html',{'country':country,'positions':positions})

