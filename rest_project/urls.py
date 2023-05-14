# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_app.views import ProductDocumentViewSet



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_app.urls'))
]