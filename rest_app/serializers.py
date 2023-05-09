import json
from .models import Product

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import ProductDocument


class ProductDocumentSerializer(DocumentSerializer):
    
    class Meta:
        """Meta options."""
        model = Product
        document = ProductDocument
        
        fields = ('title', 'price')