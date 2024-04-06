from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password
import os
from django.core import exceptions
from datetime import datetime

#user register serializer

class UserRegisterSerializer(serializers.ModelSerializer):
    print("serilizer for registering user")
    
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'phone')
        
        # create user
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
   
    
class UserLoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    
   
    def validate(self, data):
        email_or_username = data.get('email_or_username')
        password = data.get('password')
        print(data, "serializer data")
        return data
    
    
    
    
    
    
class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username', 'phone', 'first_name', 'last_name', 'email', 'profile_pic', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superuser']

        

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        # Hash the password before saving
        return make_password(value)
    
class JoiningMonthCountSerializer(serializers.Serializer):
    joining_month = serializers.SerializerMethodField()
    user_count = serializers.IntegerField()
    
    def get_joining_month(self, instance):
        month_number = instance.get('joining_month')
        current_year = instance.get('joining_year')

        if month_number is not None and current_year is not None:
            return datetime(current_year, month_number, 1).strftime('%b %Y')
        else:
            return None
    

