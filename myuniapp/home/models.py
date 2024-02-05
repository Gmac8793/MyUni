from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()    
    
    def __str__(self):
        return f'{self.name}'
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(max_length=500)
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return (f'{self.title} {self.user} {self.place}')
