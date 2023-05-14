from django.db import models


    
    
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    def __str__(self):
        return self.title