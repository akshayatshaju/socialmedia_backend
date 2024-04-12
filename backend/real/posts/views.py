from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Post, PostMedia,Comment,Like
from .serializer import PostCreationSerializer,CommentSerializer,GetPostSerializer,PostMediaSerializer
from rest_framework.permissions import  IsAuthenticated
from rest_framework.parsers import MultiPartParser
from user.models import Account
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import HashTag, Follow
from django.db.models import Q
#from chat.models import *
from .serializer import *
from django.shortcuts import get_object_or_404


class CreatePost(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data,"hhh")
       
        caption = request.data.get('caption', '')
        hashtags = request.data.get('hashtag',[])
        print(hashtags,"firsthashtaggetting")
        hashtag_instance = []
        hash = hashtags.split(',')

        for h in hash:
            hashget,hashcreate = HashTag.objects.get_or_create(hashtag=h)
            hashtag_instance.append(hashget)
            print(hashget,"kkkkk",hashtag_instance,"cheking hashtag")
        
        newrequest = request.data
        newrequest['hashtags'] = [hashget.id for hashget in hashtag_instance]



        # Assuming 'croppedImages' is the key for the images in the FormData
        print(request.FILES,"before")
        
        cropped_images = request.FILES.getlist('Images')
        print(cropped_images,"croped")

        # Create a Post instance with the caption
        post_serializer = PostCreationSerializer(data={'caption': caption,'hashtags':newrequest['hashtags']},context={'request': request})
        if post_serializer.is_valid():
            print("validddd",request.user)
            post_instance = post_serializer.save(user=request.user)

            # Save the cropped images as PostMedia instances
            for image in cropped_images:
                post_media_serializer = PostMediaSerializer(data={'media_file': image})
                print(post_media_serializer,"mediaserlizer")
                if post_media_serializer.is_valid():
                    
                    post_media_serializer.save(post=post_instance)
                    
                else:
                    # Handle invalid media file
                    print(post_media_serializer.errors)
            
            post_serializer.instance.hashtags.set(hashtag_instance)
            print(hashtag_instance,"hashyaag")
            return Response({'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Handle invalid post data
            print(post_serializer.errors)
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
class LikePost(APIView):
    permission_classes=[IsAuthenticated]
    def get_like_count(self, post):
        return Like.objects.filter(post=post).count()
    
    def post(self,request):
        try:
            print(request.data,"data")
            p = Post.objects.get(id=request.data.get('id'))
            print(p,"post to like")
            if Like.objects.filter(post=p, user=request.user).exists():
                Like.objects.get(post=p,user=request.user).delete()
                print("unlikeeeeeeee")
                like_count = self.get_like_count(p)
                return Response({"message": "You have unliked liked this post","like_count": like_count}, status=status.HTTP_200_OK)

            Like.objects.create(user=request.user,post=p)
            Notification.objects.create(
                        from_user=request.user,
                        to_user=p.user,
                        post=p,
                        notification_type=Notification.NOTIFICATION_TYPES[0][0],
                    ) 
            print("liked")
            like_count = self.get_like_count(p)
            return Response({"message": "You have liked this post","like_count": like_count}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            print("post not found")
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        

# when user comments on a post
class CommentPost(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
        try:
            # Check if the post exists
            print(request.data,"data")
            post = Post.objects.get(id=id)
            print(request.user.id,"user iddddddddd")
            # Extract comment data from the request data
            comment_data = {
                'content': request.data.get('content'),
                'post': post.id,
            }

            print(comment_data)

            # Serialize the comment data
            serializer = CommentSerializer(data=comment_data,context={'request':request})
            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                        from_user=request.user,
                        to_user=post.user,
                        post=post,
                        notification_type=Notification.NOTIFICATION_TYPES[3][0],
                    ) 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


# when user comments on a post
class CommentPost(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,id):
        try:
            # Check if the post exists
            print(request.data,"data")
            post = Post.objects.get(id=id)
            print(request.user.id,"user iddddddddd")
            # Extract comment data from the request data
            comment_data = {
                'content': request.data.get('content'),
                'post': post.id,
            }

            print(comment_data)

            # Serialize the comment data
            serializer = CommentSerializer(data=comment_data,context={'request':request})
            if serializer.is_valid():
                serializer.save()
                Notification.objects.create(
                        from_user=request.user,
                        to_user=post.user,
                        post=post,
                        notification_type=Notification.NOTIFICATION_TYPES[3][0],
                    ) 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


class GetComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Check if the post exists
            post = Post.objects.get(id=id)

            # Retrieve all comments for the post
            comments = Comment.objects.filter(post=post)

            # Serialize the comments data
            serializer = CommentSerializer(comments, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        

class DeleteComment(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request,  id):
        try:

            # Check if the comment exists
            comment = Comment.objects.get(id=id,  user=request.user)
            print(comment,"comment")
            # Delete the comment
            comment.delete()

            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found or you don't have permission to delete"}, status=status.HTTP_404_NOT_FOUND)

# get details of logged in user
class MyPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        print(user)
        p =Post.objects.filter(user=user)
        s = GetPostSerializer(instance=p,many=True,context={'request':request})
        print(s.data)
        return Response(s.data, status=200)
        

    

class DeletePost(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,id):
        try:
            print(id,"uuid")
            p = Post.objects.get(id=id)
            p.delete()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            print("post not found")
            return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
       


class RecommendedPostView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user = request.user
        print(user,user.id)

        # get hashtags of posts liked by user
        liked_post_hashtags = HashTag.objects.filter(hash__like__user=user)
        print(liked_post_hashtags,"likee")


        # find post with similar hashtags
        recommended = (Post.objects.filter(hashtags__in=liked_post_hashtags).exclude(Q(user=user)|Q(like__user=user)).distinct())
        print(recommended,"recomended")

        remaining = Post.objects.exclude(Q(user=user)|Q(id__in=recommended.values('id')))
        print(remaining,"remainggg")
        
        remaining_serializer = GetPostSerializer(instance=remaining,many=True,context={'request':request})
        recommended_serializer = GetPostSerializer(instance=recommended,many=True,context={'request':request})
        print(remaining_serializer, "reserilizer")
        print(recommended_serializer, "recomserilizer")

        combined = recommended_serializer.data + remaining_serializer.data
        print(combined,"combined")
        return Response(combined,status=200)
    


class Likecount(APIView):
    def get(self,request):
        p = Post.objects.filter(user=request.user)
        like_count = Like.objects.filter(post=p)
        return Response({'like-count':like_count},status=200)



#-------------------------following/followers------------------------------------------#



class FollowUnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        logged_in_user = request.user
        try:
            user_to_follow = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if logged_in_user == user_to_follow:
            return Response(
                {"detail": "You cannot follow/unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            follow_instance = Follow.objects.get(
                follower=logged_in_user, following=user_to_follow
            )
            follow_instance.delete()
            print("unfollwedd")
            return Response(
                {"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK
            )
        except Follow.DoesNotExist:
            follow_instance = Follow(follower=logged_in_user, following=user_to_follow)
            follow_instance.save()
            print("followed",follow_instance)
            n=Notification.objects.create(
                        from_user=request.user,
                        to_user=user_to_follow,
                        notification_type=Notification.NOTIFICATION_TYPES[2][0],
                    ) 
            print(n)
            return Response(
                {"detail": "You are now following this user."},
                status=status.HTTP_201_CREATED,
            )
    
    
# class ContactListvView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]

#     def retrieve(self, request, *args, **kwargs):
#         user = self.request.user
#         followers = user.followers.all()
#         following = user.following.all()
#         unique_user_ids = set()
#         response_data = []
        
#         for follower in followers:
#             if follower.follower.id not in unique_user_ids and follower.follower != user:
#                 follower_data = {
#                     "id": follower.follower.id,
#                     "username": follower.follower.username,
#                     "profile_pic": follower.follower.profile_pic.url
#                         if follower.follower.profile_pic else None,
#                     "last_login": follower.follower.last_login,
#                 }
#                 # Count unread messages for this follower
#                 unread_message_count = Message.objects.filter(
#                     room__members=user, sender=follower.follower, is_seen=False
#                 ).count()
#                 follower_data["unseen_message_count"] = unread_message_count
#                 response_data.append(follower_data)
#                 unique_user_ids.add(follower.follower.id)
        
#         for followed in following:
#             print(followed.following)

#             if followed.following.id not in unique_user_ids and followed.following != user:
#                 print(followed,"following")
#                 following_data = {
#                     "id": followed.following.id,
#                     "username": followed.following.username,
#                     "profile_pic": followed.following.profile_pic.url
#                         if followed.following.profile_pic else None,
#                     "last_login": followed.following.last_login,
#                 }
#                 # Count unread messages for this followed user
#                 unread_message_count = Message.objects.filter(
#                     room__members=user, sender=followed.following, is_seen=False
#                 ).count()
#                 following_data["unread_message_count"] = unread_message_count
#                 response_data.append(following_data)
#                 unique_user_ids.add(followed.following.id)

#         return Response(response_data)
    
    
class FollowingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        user = Account.objects.get(id=user_id)
        return Follow.objects.filter(follower=user)
    

class FollowerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        user = Account.objects.get(id=user_id)
        return Follow.objects.filter(following=user)


    
    