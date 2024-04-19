from django.db import models
from user.models import Account
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.ForeignKey(Account,related_name='myposts', on_delete=models.CASCADE)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashtags = models.ManyToManyField('HashTag',related_name='hash')

    def __str__(self):
        return f"{self.user.username} ---- {self.caption} ---- {self.created_at}"
    
    
class PostMedia(models.Model):
    post = models.ForeignKey(Post, related_name='post_media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='post_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.user.username}-{self.post.caption}-{self.media_file} - {self.uploaded_at}"



class Like(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    
class Comment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content =  models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)

class HashTag(models.Model):
    hashtag = models.CharField(null=True,max_length=50)
    def __str__(self):
        return self.hashtag
    
    
class Follow(models.Model):
    follower = models.ForeignKey(
        Account, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        Account, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()




class SavedPost(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  

    class Meta:
        unique_together = ('user', 'post') 





class Notification(models.Model):
   NOTIFICATION_TYPES = [
        ('like', 'New Like'),
        ('post', 'New Post'),
        ('follow', 'New Follow'),
        ('comment', 'New Comment'),
       
    ]
   
   from_user = models.ForeignKey(Account, related_name="notification_from", on_delete=models.CASCADE, null=True)
   to_user = models.ForeignKey(Account, related_name="notification_to", on_delete=models.CASCADE, null=True)
   notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=20)
   post  = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
   comment  = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
   created = models.DateTimeField(auto_now_add=True)
   is_seen = models.BooleanField(default=False)
   
   def __str__(self):
        return f"{self.from_user} sent a {self.notification_type} notification to {self.to_user}"







# Create your models here.
