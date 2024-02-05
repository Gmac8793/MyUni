from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from social_app.forms import *
import json
from urllib.parse import unquote
from home.models import Post, Place

# Create your views here.
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        else:
            form = PostForm()
            
    return render(request, 'home/post.html', {'form': form})

def feed(request):
    place_id = request.GET.get('id')
    place = get_object_or_404(Place, id=place_id)
    
    posts = Post.objects.filter(place=place)
    #posts = Post.objects.all()
    #post_titles = [post.title for post in posts]
    
    return render(request, 'social_app/feed.html', {'place': place, 'posts': posts})

    #return render(request, 'social_app/feed.html', {'titles': json.dumps(titles)})
    
    

    '''
    if request.method == 'POST':
        content = request.POST.get('content')
        post = Post.objects.create(place=place, content=content)
        
    return render(request, 'social_app/feed_page.html', {'place': place, 'posts': posts})
    '''