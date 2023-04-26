from django.db import models, transaction

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/products/original",null=True, blank=True)
    thumbnail = models.ImageField(upload_to="images/products/thumbnail", null=True, blank=True)
    
    def __str__(self):
        return self.name