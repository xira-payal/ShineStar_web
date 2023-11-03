from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.name
