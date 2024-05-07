from django.contrib import admin
from home.models import Profile, Post, PostComment, Reply, LikedPost, LikedComment

# Register your models here.
admin.site.register(Profile)
admin.site.register(PostComment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
