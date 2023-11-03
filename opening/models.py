from django.db import models
from country.models import Country
# Create your models here.
class Opening(models.Model):
    position = models.CharField(max_length=255)
    vaccancy = models.IntegerField()
    salary = models.IntegerField()
    description = models.CharField(max_length=255)
    location = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.position




