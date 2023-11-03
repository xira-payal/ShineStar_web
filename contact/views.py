from django.shortcuts import render, redirect
from .models import Contact
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections

def contact_page(request):
    contact = Contact.objects.all()
    paginator = Paginator(contact, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'backend-template/contact.html',{'page_obj':page_obj})

def add_contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        try:
            Required(name,'name')
            Required(email,'email')
            Required(phone,'phone')
            Required(message,'message')
            contact = Contact(name=name,email=email,phone=phone,message=message)
            contact.save()
            return redirect('contact')
        except ValidationError as e:
            messages.error(request,str(e))
    return render(request,'backend-template/contact_add.html')

def update_contact_page(request, pk):
    if pk == pk:
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            contact = None

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            if contact:
                contact.name = name
                contact.email = email
                contact.phone = phone
                contact.message = message
                contact.save()
                return redirect('contact')
            else:
                contact = Contact.objects.create(pk=pk,name=name,email=email,phone=phone,message=message)
                contact.save()
                return redirect('contact')
    else:
        pass

    return render(request, 'backend-template/contact_update.html', {'contact': contact})

def delete_contact_page(request, pk):
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    return redirect('contact')