from django.urls import path
from rest_framework import routers

from .views import Product_get_post, Product_pk, ProductDocumentView

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'search', ProductDocumentView, basename='search')

urlpatterns = [
    path('',Product_get_post),
    path('<int:pk>',Product_pk),
    
]
urlpatterns += router.urls
