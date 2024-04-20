from django.contrib import admin
from posts.models import Post,PostMedia,Like,Comment,HashTag,Follow,SavedPost,Notification,Reply

# Register your models here.
admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Comment)
admin.site.register(HashTag)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(SavedPost)
admin.site.register(Notification)
admin.site.register(Reply)






