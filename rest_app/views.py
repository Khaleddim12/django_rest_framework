from django.http import Http404
from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Q
from .models import Product
from .serializers import ProductSerializer
from rest_framework.parsers import JSONParser ,MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from .documents import ProductDocument
from rest_framework.viewsets import ModelViewSet

# Create your views here.

@api_view(['GET', 'POST'])
@parser_classes([JSONParser, MultiPartParser])
def product_get_post(request):
    """
    List all  Product, or create a new Product.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # check if image and thumbnail files are present in request.FILES
            if 'image' in request.FILES:
                serializer.validated_data['image'] = request.FILES['image']
            if 'thumbnail' in request.FILES:
                serializer.validated_data['thumbnail'] = request.FILES['thumbnail']
            serializer.save()
            return Response({"success": True, "data": serializer.data, "message": "Product created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
@parser_classes([JSONParser, MultiPartParser])
def product_pk(request, pk):
    """
    Retrieve, update or delete a product.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            # check if image and thumbnail files are present in request.FILES
            if 'image' in request.FILES:
                serializer.validated_data['image'] = request.FILES['image']
            if 'thumbnail' in request.FILES:
                serializer.validated_data['thumbnail'] = request.FILES['thumbnail']
            serializer.save()
            return Response({"success": True, "data": serializer.data, "message": "Product edited successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"success": True,"message": "Product deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    


def generate_q_expression(query):
    return Q("match", name={"query": query, "fuzziness": "auto"})



@api_view(['GET'])
def search_results(query):
    serializer_class = ProductSerializer
    document_class = ProductDocument
    
    q = generate_q_expression(query= query)
    search = document_class.search().query(q)
    return Response(serializer_class(search.to_queryset(), many=True).data)