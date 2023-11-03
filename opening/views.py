from django.shortcuts import render , redirect
from django.http import HttpResponseServerError
from .models import Opening
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Country 
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections

def opening_page(request):
    opening = Opening.objects.all()
    paginator = Paginator(opening, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'backend-template/opening.html',{'page_obj':page_obj})

def add_opening_page(request):
    if request.method == 'POST':
        position = request.POST.get('position')
        vaccancy = request.POST.get('vaccancy')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        status = request.POST.get('status')
        location = request.POST.get('location') 
        if status == 'on':
            status = True
        else:
            status = False 

        try:
            Required(position, 'position')
            Required(vaccancy, 'vaccancy')
            Required(salary, 'salary')
            Required(description, 'description')
            location = Country.objects.get(pk=location)
            opening = Opening(position=position, vaccancy=vaccancy, salary=salary, description=description, location=location ,status=status)
            opening.save()

            return redirect('opening')
        except ValidationError as e:
            messages.error(request, str(e))
    
    countries = Country.objects.all()
    return render(request, 'backend-template/opening_add.html',{'countries':countries})

def update_opening_page(request, pk):
    try:
        opening = Opening.objects.get(pk=pk)
    except Opening.DoesNotExist:
        opening = None

    if request.method == 'POST':
        position = request.POST.get('position')
        vaccancy = request.POST.get('vaccancy')
        salary = request.POST.get('salary')
        location = request.POST.get('location') 
        description = request.POST.get('description')
        status = request.POST.get('status')

        status = (status == 'on')

        if opening:
            opening.position = position
            opening.vaccancy = vaccancy
            opening.salary = salary

            location = Country.objects.get(pk=location)
            opening.location = location

            opening.description = description
            opening.status = status

            try:
                opening.save()
            except Exception as e:
                return HttpResponseServerError("An error occurred while saving the data.")

            return redirect('opening')
    else:
        countries = Country.objects.all()
        return render(request, 'backend-template/opening_update.html', {'opening': opening, 'countries': countries})


def delete_opening_page(request,pk):
    opening = Opening.objects.get(pk=pk)
    opening.delete()
    return redirect('opening')


