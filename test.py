import os
import django

# set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_project.settings')

# initialize Django
django.setup()

# import models and use them
from rest_app.models import Product
from rest_app.documents import ProductDocument


product = Product(name='marwan', salary="100000000")
product.save()

productdoc = ProductDocument.search().filter("term", name = "khaled")

""" for hit in empdoc:
    print(
        "product name : {}, salary {}".format(hit.name, hit.salary)
    )
     """

#convert the elastisearch result into a real django queryset
qs = productdoc.to_queryset()

for prod in qs:
    print(prod.name)