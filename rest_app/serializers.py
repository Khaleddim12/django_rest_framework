from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, FloatField


class EmployeeSerializer(serializers.ModelSerializer):
    name = CharField(required=True)
    salary = FloatField(required=True)
    
    class Meta:
        model = models.Employee
        fields = "__all__"