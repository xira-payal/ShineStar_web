from django.shortcuts import render, redirect,  get_object_or_404
from .models import Contact
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections


@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def contact_page(request):
    contact = Contact.objects.all()
    paginator = Paginator(contact, 8) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'cms/contact.html',{'page_obj':page_obj})


@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
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
            messages.success(request, "Contact added successfully")
            return redirect('contact')
        except ValidationError as e:
            messages.error(request,str(e))
    return render(request,'cms/contact_add.html')


@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
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
                messages.info(request, "Contact update successfully")
                return redirect('contact')
            else:
                contact = Contact.objects.create(pk=pk,name=name,email=email,phone=phone,message=message)
                contact.save()
                messages.info(request, "Contact update successfully")
                return redirect('contact')
    else:
        pass

    return render(request, 'cms/contact_update.html', {'contact': contact})



@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def delete_contact_page(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact = Contact.objects.get(pk=pk)
    contact.delete()
    messages.warning(request, "Contact deleted successfully")
    return redirect('contact')


def contact_pages(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        try:
            contact = Contact(name=name,email=email,phone=phone,message=message)
            contact.save()
            messages.success(request, 'Your contact information has been successfully submitted.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    return render(request, 'web/contact-us.html')

