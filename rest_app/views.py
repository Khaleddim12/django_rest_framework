from django.shortcuts import get_object_or_404

from rest_framework.parsers import JSONParser ,MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view

from .serializers import ProductDocumentSerializer
from .models import Product
from .documents import ProductDocument
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    SimpleQueryStringSearchFilterBackend
)

from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

# Create your views here.


class ProductViewSet(DocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    ordering = ('id',)
    lookup_field = 'id'
    
    filter_backends = [
        DefaultOrderingFilterBackend,
        FilteringFilterBackend,
        SimpleQueryStringSearchFilterBackend,
    ]
    
    search_fields = (
        'title',        
    )
    
    filter_fields = {
        'id': 'id',
        'title': 'title',
        'price': {
            'field': 'price',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        }
    }
    
    suggester_fields = {
        'title_suggest': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }


# Create your views here.


@api_view(['GET', 'POST'])
@parser_classes([JSONParser, MultiPartParser])
def Product_get_post(request):
    """
    List all Product, or create a new Product.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductDocumentSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductDocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the Product instance from the validated data
            product_instance = serializer.save()
            
            # Explicitly save the new Product instance to the database
            product_instance.save()
            
            # Use the product instance in the response data
            return Response({"success": True, "data": {
                "title": product_instance.title,
                "price": product_instance.price
            }, "message": "Product created successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def Product_pk(request, pk):
    """
    Retrieve, update or delete a Product.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductDocumentSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductDocumentSerializer(product, data=request.data)
        if serializer.is_valid():
            # check if image and thumbnail files are present in request.FILES
            serializer.save()
            return Response({"success": True, "data": serializer.data, "message": "Product edited successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"success": True,"message": "Product deleted successfully."},status=status.HTTP_204_NO_CONTENT)