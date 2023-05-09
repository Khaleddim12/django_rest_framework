from django.urls import path
from .views import Product_get_post, Product_pk, ProductSearch, ProductDocumentViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register('products', ProductDocumentViewSet, basename='product')
urlpatterns = [
    path('', Product_get_post),
    path('<int:pk>', Product_pk),
    path('search/<str:query>/', ProductSearch.as_view()),
]

urlpatterns += router.urls