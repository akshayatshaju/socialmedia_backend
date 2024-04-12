from django.urls import path
from .views import UserRegisterView, UserLoginView, GetUserView,CheckAuth, ChangeProfilePicView, EditProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user',GetUserView.as_view(),name='user'),
    path('check-auth/', CheckAuth, name='check-auth'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    path('changeprofile',ChangeProfilePicView.as_view(),name='changeprofile'),
    path('editprofile',EditProfileView.as_view(),name='editprofile'),
    
  
]
