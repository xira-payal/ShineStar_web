from .models import Blogs
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


def blog_page(request):
    blogs = Blogs.objects.all()
    paginator = Paginator(blogs, 4) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'backend-template/blog.html', {'page_obj': page_obj})

def add_blog_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        content = request.POST.get('content')
        try:
            Required(title,'title')
            Required(image,'image')
            Required(content,'content')
            Validate_img_extension(image)
            blogs = Blogs(title=title,image=image,content=content)
            blogs.save()
            return redirect('blog')
        
        except ValidationError as e:
            messages.error(request,str(e))
    else:
        pass
    return render(request,'backend-template/blog_add.html')

def update_blog_page(request, pk):
    if pk == pk:
        try:
            blog = Blogs.objects.get(pk=pk)
        except Blogs.DoesNotExist:
            blog = None

        if request.method == 'POST':
            title = request.POST.get('title')
            image = request.FILES.get('image')
            content = request.POST.get('content')

            if blog:
                if image:
                    if blog.image:
                        os.remove(blog.image.path)
                    blog.image = image
                blog.title = title
                blog.content = content
                blog.save()
                return redirect('blog')
            else:
                blog = Blogs.objects.create(pk=pk, title=title, image=image, content=content)
                blog.save()
                return redirect('blog')
    else:
        pass

    return render(request, 'backend-template/blog_update.html', {'blogs': blog})

def delete_blog_page(request, pk):
    blog = Blogs.objects.get(pk=pk)
    blog.delete()
    return redirect('blog')

def go_back(request):
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)