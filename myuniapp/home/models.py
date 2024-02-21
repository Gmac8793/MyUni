from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-profile.png')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username

class Place(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()    
    
    def __str__(self):
        return f'{self.name}'
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images', blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(max_length=500)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    
    
    def __str__(self):
        return (f'{self.title} {self.user} {self.place}')

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)