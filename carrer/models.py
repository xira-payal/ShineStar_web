from django.db import models

# Create your models here.
class Carrer(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.IntegerField()
    address = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    experiance = models.CharField(max_length=255)
    files = models.FileField(upload_to='uploads/')
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.firstname

