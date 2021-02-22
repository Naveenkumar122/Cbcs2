from rest_framework import serializers
from .models import admin_detail

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin_detail
        fields = ['id', 'username', 'password', 'role','mobile']

