from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registeredUsers',RegisteredUsers.as_view(),name='registeredUsers'),
    path('userdetail/<str:userEmail>/', UserDetail.as_view(), name='userdetail'),
    
   
    path('deleteuser/<int:id>/', DeleteUser.as_view(), name='deleteuser'),

    path('blockuser/<int:id>/',BlockUser.as_view(),name='blockuser'),
    
    path('adminuserposts/<str:userEmail>/',AdminUserPosts.as_view(),name='adminuserposts'),
    path('adminuserpostsdetails/<uuid:id>/',AdminUserPostsDetails.as_view(),name='adminuserpostsdetails'),
    path('deletepost/<uuid:id>/',DeletePost.as_view(),name='deletepost'),
    path('deletecomment/<int:id>/',DeleteComment.as_view(),name='deletecomment'),
    
    
    path('graph',UserCountByMonth.as_view(),name='graph'),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
