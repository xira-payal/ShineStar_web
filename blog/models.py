from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify 
from django.utils.text import slugify
import uuid

# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    content = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True,null=True)

    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     if not self.slug or Blogs.objects.filter(slug=self.slug).exists():
    #         self.slug = slugify(self.title) + f"-{uuid.uuid4().hex[:6]}"
    #     super().save(*args, **kwargs)


        
