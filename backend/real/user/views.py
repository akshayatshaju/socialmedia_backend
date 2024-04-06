from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer,UserLoginSerializer,GetUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
#from rest_framework import permissions,generics
from rest_framework.authentication import authenticate
# from django.contrib.auth import authenticate
from .models import Account
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
#from django.db.models import Count,Q
#from django.db.models.functions import ExtractMonth, ExtractYear
#from django.utils import timezone


#User Register view

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data,"serializer data")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

   
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_username = serializer.validated_data.get('email_or_username')
            password = serializer.validated_data.get('password')
            print(email_or_username, password)
            # Authenticate user
            
            try:
                # authenticate with email or username
                user = authenticate(request, username=email_or_username, password=password)
                print(user)
                
                # if user instance is returned and create token and considered as user logged in
                if user:
                    if user.is_deleted:
                        return Response({"details": "This account has been deleted."}, status=401)

                    print("success login")
                    refresh = RefreshToken.for_user(user)
                    refresh['email'] = user.email
                    refresh['is_superuser'] = user.is_superuser
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return Response(
                        {
                            "email_or_username": email_or_username,
                            "password": password,
                            "access": access_token,
                            "refresh": refresh_token,
                        },
                        status=201,
                    )
                else:
                    # If user is None, wrong email or password
                    return Response({"details": "Invalid email or password"}, status=401)

            except Account.DoesNotExist:
                # If user doesn't exist, wrong email or password
                return Response({"details": "no user email or password"}, status=401)




        
    
    
# get details of logged in user
class GetUserView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
 
    def get(self,request):
    
        user_email = request.user
        print(request.user)
        user_details = Account.objects.get(email=user_email)
        serializer = GetUserSerializer(instance=user_details)
        print(serializer.data)
        return Response(serializer.data,status=200)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CheckAuth(request):
    # If the view reaches here, the user is authenticated
    return Response({'message': 'Authenticated'})
    