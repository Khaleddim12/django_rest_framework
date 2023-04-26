from django.urls import path
from rest_framework import routers

from .views import product_get_post, product_pk, search_results


urlpatterns = [
    path('', product_get_post),
    path('<int:pk>', product_pk),
    path('product_search/<str:query>/', search_results)
]
