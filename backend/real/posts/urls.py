from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('mypost/',MyPostView.as_view(),name='mypost'),
    path('createpost',CreatePost.as_view(),name='createpost'),
    path('deletepost/<uuid:id>/', DeletePost.as_view(), name='deletepost'),
    path('recommended/', RecommendedPostView.as_view(), name='recommended'),
     
    path('likepost', LikePost.as_view(), name='likepost'),
    path('likecount', Likecount.as_view(), name='likecount'),
     
     
    path('commentpost/<uuid:id>/', CommentPost.as_view(), name='commentpost'),
    path('comments/<uuid:id>/', GetComments.as_view(), name='comments'),
    path('deletecomment/<int:id>/', DeleteComment.as_view(), name='deletecomment'),
    
    
    path('follow/<int:user_id>/', FollowUnfollowUserView.as_view(), name='follow-user'),
    path('followings/<int:id>/', FollowingListView.as_view(), name='following-list'),
    path('followers/<int:id>/', FollowerListView.as_view(), name='follower-list'),

]