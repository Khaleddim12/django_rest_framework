from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=200,unique=True)
    salary = models.FloatField()
    
    def __str__(self):
        return self.name