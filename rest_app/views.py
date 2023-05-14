from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search

from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer

from .serializers import ProductDocumentSerializer, ProductSerializer
from .models import Product
from .documents import ProductDocument

from rest_framework.views import APIView
from rest_framework_json_api.views import ModelViewSet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from django_elasticsearch_dsl_drf.filter_backends import (
    OrderingFilterBackend,
    CompoundSearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet


from rest_app.documents import ProductDocument

class ProductDocumentViewSet(DocumentViewSet):
    document = ProductDocument
    serializer_class = ProductDocumentSerializer

    filter_backends = (
        CompoundSearchFilterBackend,
        SuggesterFilterBackend,
        OrderingFilterBackend,
        DjangoFilterBackend,
    )

    search_fields = ("title",)

    ordering_fields = {
        "id": None,
    }

    filter_fields = {
        "title": "title",
        "price": {
            "field": "price.raw",
            "lookups": [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
    }

    suggester_fields = {
        "title_suggest": {
            "field": "title.suggest",
            "suggesters": [SUGGESTER_COMPLETION],
        }
    }


class ProductSearch(APIView):
    serializer_class = ProductSerializer
    document_class = ProductDocument

    def generate_q_expression(self, query):
        return Q("match", title={"query": query, "fuzziness": "auto"})

    def get(self, request, query):
        q = self.generate_q_expression(query)
        search = self.document_class.search().query(q)
        return Response(self.serializer_class(search.to_queryset(), many=True).data)


@api_view(["GET", "POST"])
@parser_classes([JSONParser, MultiPartParser])
def Product_get_post(request):
    """
    List all Product, or create a new Product.
    """
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            # Create the Product instance from the validated data
            product_instance = serializer.save()
            
            # Explicitly save the new Product instance to the database
            product_instance.save()
            
            
            # Use the product instance in the response data
            return Response(
                {
                    "success": True,
                    "data": {
                        "title": product_instance.title,
                        "price": product_instance.price,
                    },
                    "message": "Product created successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@parser_classes([JSONParser])
def Product_pk(request, pk):
    """
    Retrieve, update or delete a Product.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            # check if image and thumbnail files are present in request.FILES
            serializer.save()
            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "message": "Product edited successfully.",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(
            {"success": True, "message": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
