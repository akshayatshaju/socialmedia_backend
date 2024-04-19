from rest_framework import serializers

from posts.models import Follow
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
    
    
    
    
    
    
# class GetUserSerializer(serializers.ModelSerializer):
    

    
    
#     class Meta:
#         model = Account
#         fields = ['id',
#                   'username',
#                   'phone', 
#                   'first_name',
#                   'last_name', 'email', 
#                   'profile_pic', 
#                   'date_joined', 
#                   'last_login',
#                   'is_admin',
#                   'is_staff', 
#                   'is_active', 
#                   'is_superuser',
                  
#                   ]
class GetUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    # is_following = serializers.SerializerMethodField()
    posts_count =  serializers.SerializerMethodField()

 
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.following.count()  
    
    # def get_is_following(self, obj):
    #     print(Follow.objects.filter(follower=self.context['request'].user, following=obj))
    #     return Follow.objects.filter(follower=self.context['request'].user, following=obj).exists()
    
    def get_posts_count(self, obj):
        return obj.myposts.count()  
    
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "first_name",
            "username",
            "email",
            'phone',
            "profile_pic",
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "followers_count",
            "followings_count",
        
            'posts_count'
            
        ]
        

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
    

