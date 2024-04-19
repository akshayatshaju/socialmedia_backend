from rest_framework import serializers
from posts.models import *
from user.serializers import GetUserSerializer
from django.contrib.auth.models import AnonymousUser

class PostMediaSerializer(serializers.ModelSerializer):
    media_file = serializers.FileField(max_length=None, use_url=True)

    class Meta:
        model = PostMedia
        fields = ['id', 'media_file', 'uploaded_at']

class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = '__all__'
        
class GetPostSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, read_only=True)
    hashtags = HashTagSerializer(many=True,read_only=True)
    user=GetUserSerializer(read_only=True)
    is_following_author = serializers.SerializerMethodField()
    is_liked_or_not = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    saved_or_not = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'created_at', 'updated_at', 'post_media','hashtags','is_following_author',
                  'is_liked_or_not','like_count','saved_or_not'
                  ]
    

    def get_user(self,obj):
        instance = obj.user
        user_ser = GetUserSerializer(instance)
        return user_ser.data

    
    
    def get_is_following_author(self, obj):
        request_user = self.context['request'].user
        user = obj.user
        if request_user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=request_user, following=user)
                return True
            except Follow.DoesNotExist:
                return False
        return False
    

    def get_is_liked_or_not(self, obj):
        request_user = self.context['request'].user
        user = obj.user
        if request_user.is_authenticated:
            try:
                like_instance = Like.objects.get(user=request_user, post=obj)
                return True
            except Like.DoesNotExist:
                return False
        return False

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()



    def get_saved_or_not(self,obj):
        request_user = self.context['request'].user
        if request_user.is_authenticated:
            try:
                save_instance = SavedPost.objects.get(user=request_user,post=obj)
                return True
            except SavedPost.DoesNotExist:
                return False
        return False



class PostCreationSerializer(serializers.ModelSerializer):
    hashtags = HashTagSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ['caption', 'user','hashtags']
        read_only_fields = ['user']  # Make the user field read-only

    def validate(self, data):
        # Check if the user is authenticated
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            raise serializers.ValidationError("User must be authenticated to create a post.")

        # Set the user field to the current authenticated user
        data['user'] = user
        return data

    

class CommentSerializer(serializers.ModelSerializer):
   
    user=GetUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','content', 'commented_at', 'user','post')
        

    def create(self, validated_data):
        user = self.context['request'].user


        # Create the comment with the extracted user instance
        comment = Comment.objects.create(user=user, **validated_data)
        return comment
    def get_user(self,obj):
        print("object")
        instance = obj.user
        print(instance,"instance")
        user_ser = GetUserSerializer(instance)
        return user_ser.data
    
    
class ReplySerializer(serializers.ModelSerializer):
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'content', 'replied_at', 'user', 'comment')

    def create(self, validated_data):
        user = self.context['request'].user
        comment_id = self.context['comment_id']  # Assuming you pass comment_id in context

        # Create the reply with the extracted user instance and comment id
        reply = Reply.objects.create(user=user, comment_id=comment_id, **validated_data)
        return reply

    
#-----------------------------------------------------------------------------------------------------------------------------------
class AccountSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    posts_count =  serializers.SerializerMethodField()

 
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.following.count()  
    
    def get_is_following(self, obj):
        print(Follow.objects.filter(follower=self.context['request'].user, following=obj))
        return Follow.objects.filter(follower=self.context['request'].user, following=obj).exists()
    
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
            'is_following',
            'posts_count'
            
        ]




class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field="email", queryset=Account.objects.all()
    )
    follower = serializers.SlugRelatedField(
        slug_field="email", queryset=Account.objects.all()
    )

    class Meta:
        model = Follow
        fields = ["follower", "following", "created_at"]



# serializers.py

class FollowerSerializer(serializers.ModelSerializer):
    follower = AccountSerializer(read_only=True)
    is_following_follower = serializers.SerializerMethodField()

    def get_is_following_follower(self, obj):
        user = self.context['request'].user
        follower = obj.follower
        if user.is_authenticated:
            try:
                follow_instance = Follow.objects.get(follower=user, following=follower)
                return True
            except Follow.DoesNotExist:
                return False
        return False

    class Meta:
        model = Follow
        fields = ["follower", "created_at", "is_following_follower"]


class FollowingSerializer(serializers.ModelSerializer):
    following = AccountSerializer( read_only=True)

    class Meta:
        model = Follow
        fields = ["following", "created_at"]



class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = '__all__'




class NotificationSerializer(serializers.ModelSerializer):
    from_user = AccountSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('notification_type',)

    def validate_notification_type(self, value):
        choices = dict(Notification.NOTIFICATION_TYPES)
        if value not in choices:
            raise serializers.ValidationError("Invalid notification type.")
        return value