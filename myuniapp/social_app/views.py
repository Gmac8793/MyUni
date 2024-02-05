from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from social_app.forms import *
import json
from urllib.parse import unquote
from home.models import Post, Place

# Create your views here.
def create_post(request, place_id):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            #post = form.save(commit=False) 
            post = Post.objects.create(
                user = request.user,
                content = request.POST.get("content"),
                title = request.POST.get("title"),
                place = Place.objects.get(pk=place_id)
            )
            #post.user = request.user
            #post.save()
            return redirect('home')
        else:
            form = PostForm()
            
    return render(request, 'home/post.html', {'form': form})

def feed(request):
    place_id = request.GET.get('id')
    place = get_object_or_404(Place, id=place_id)
    
    posts = Post.objects.filter(place=place)
    
    
    return render(request, 'social_app/feed.html', {'place': place, 'posts': posts})
