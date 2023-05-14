from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from .documents import ProductDocument
from .models import Product
from elasticsearch_dsl.utils import AttrDict


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price')


class ProductDocumentSerializer(DocumentSerializer):
    
    class Meta:
        document = ProductDocument
        fields = ('id', 'title', 'price')
