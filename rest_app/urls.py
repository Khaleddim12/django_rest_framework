from django.urls import path

from .views import *

urlpatterns = [
    path('', employee_get_post,name = 'employeeView'),
    path('<int:pk>', employee_pk,name='EmployeeInfo'),
]