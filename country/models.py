from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name