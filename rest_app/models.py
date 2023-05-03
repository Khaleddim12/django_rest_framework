from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=50.0)
    
    def __str__(self):
        return self.title