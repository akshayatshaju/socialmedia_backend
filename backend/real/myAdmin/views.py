from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.serializers import UserRegisterSerializer, UserLoginSerializer, GetUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import permissions
from rest_framework.authentication import authenticate
# from django.contrib.auth import authenticate
from user.models import Account
from rest_framework_simplejwt.authentication import JWTAuthentication
#from posts.models import *
#from posts.serializer import *
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay,TruncDate,TruncMonth,TruncYear
from django.db.models import F,Q ,Count
from user.serializers import JoiningMonthCountSerializer
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist


#get all registerd user
class RegisteredUsers(APIView):
 
    def get(self,request):
        users = Account.objects.filter(is_superuser=False)
        serializer = GetUserSerializer(instance=users, many=True)
        print(serializer)
        return Response(serializer.data,status=200)
    
# get details of user with a  email
# class UserDetail(APIView):
 
#     def get(self,request,userEmail):
#         print(" requested for details of user")
#         detail = Account.objects.get(email=userEmail)
#         print(detail, "hgfhfyh")
#         serializer = GetUserSerializer(instance=detail)
#         print(serializer.data, "getttt")
#         return Response(serializer.data,status=200)

class UserDetail(APIView):
    def get(self, request, userEmail):
        try:
            # print("Requested details of user:", userEmail)
            detail = Account.objects.get(email=userEmail)
            # print(detail,"userdetaill")
            serializer = GetUserSerializer(instance=detail)
            # print(serializer.data)
            return Response(serializer.data, status=200)
        except ObjectDoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"error": "Internal Server Error"}, status=500)
    
# delete user with id
# class DeleteUser(APIView):
   
#     def patch(self, request, id):
#         try:
#             user = Account.objects.get(id=id)
#             print(user, "user id gett")
#             user.is_deleted = True
#             user.save()
#             return Response({"message": "success"}, status=status.HTTP_200_OK)
#         except Account.DoesNotExist:
#             print("user not found")
#             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)






# block user with id
class BlockUser(APIView):
    def patch(self, request, id):
        try:
            user = Account.objects.get(id=id)
            print(user.is_active,"in block fun checking user")
            b = user.is_active
            user.is_active = not b
            print(user.is_active,"after change")
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# delete user with id
class DeleteUser(APIView):
   
    def patch(self, request, id):
        try:
            user = Account.objects.get(id=id)
            user.is_deleted = True
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            print("user not found")
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# block user with id
class BlockUser(APIView):
    def patch(self, request, id):
        try:
            user = Account.objects.get(id=id)
            print(user.is_active,"in block fun checking user")
            b = user.is_active
            user.is_active = not b
            print(user.is_active,"after change")
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserCountByMonth(APIView):
       def get(self, request):
        user_counts = (
            Account.objects.annotate(
                joining_month=ExtractMonth('date_joined'),
                joining_year=ExtractYear('date_joined')
            )
            .values('joining_month', 'joining_year')
            .annotate(user_count=Count('id'))
            .order_by('joining_year', 'joining_month')
        )
        serializer = JoiningMonthCountSerializer(user_counts, many=True)

        return Response(serializer.data)