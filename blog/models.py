from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    content = models.CharField(max_length=255)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

