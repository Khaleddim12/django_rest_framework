# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers



urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('rest_app.urls'))
]

