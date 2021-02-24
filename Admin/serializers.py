from rest_framework import serializers
from .models import *

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin_detail
        fields = ['id', 'username', 'password', 'role','mobile']

#serializer for student module

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = student_detail
        fields = ['id','Rollno','Name','Type','Batch']