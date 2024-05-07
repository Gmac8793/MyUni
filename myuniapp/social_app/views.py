from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from social_app.forms import *
from django.db.models import Count
import json
from home.models import *

# Create your views here.
def create_post(request, place_id):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(
                user = request.user,
                content = request.POST.get("content"),
                title = request.POST.get("title"),
                place = Place.objects.get(pk=place_id)
            )
            if 'image' in request.FILES:
                post_image = PostImage(post=post, image=request.FILES['image'])
                post_image.save()
            
            return redirect('home')
        else:
            form = PostForm()
            
    return render(request, 'home/post.html', {'form': form})

def create_event(request, place_id):
    place = Place.objects.get(pk=place_id) 
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.place = place
            event.user = request.user
            event.save()
        
        
        if 'event_image' in request.FILES:
            event_image = EventImage(event=event, image=request.FILES['event_image'])
            event_image.save()
            
        place.is_event = True
        place.save()
        messages.success(request, 'Event added successfully.')
        return redirect('home')

     
    else:
        form = EventForm()   
    return render(request, 'social_app/event.html', {'form': form})

def show_event(request):
    current_time = timezone.now()
    events = Event.objects.filter(end_date__gte=current_time)
    events_data = []
    
    for event in events:
        event_images = event.images.all()
        image_urls = [image.image.url for image in event_images]
        
        event_data = {
            'title': event.title,
            'detail': event.detail,
            'date': [event.start_date, event.end_date],
            'image_urls': image_urls
        }
        events_data.append(event_data)
        
    return render(request, 'social_app/show_event.html', {'events_data': events_data})
        
@login_required(login_url='/login/')
def feed(request):
    place_id = request.GET.get('id')
    place = get_object_or_404(Place, id=place_id)
    posts = Post.objects.filter(place=place)
    profile = request.user.profile
    
    events = Event.objects.filter(place=place, end_date__gte=timezone.now())

    
   

    return render(request, 'social_app/feed.html', {'place': place, 'posts': posts, 'events': events, 'profile': profile})


def post_content(request, post_id):
    post = Post.objects.get(pk=post_id)
    commentform = CommentForm()
    replyform = ReplyForm()
    
    profile = request.user.profile
    
    context = {
        'post': post, 
        'commentform': commentform,
        'profile': profile,
        'post_id': post_id,
        'replyform': replyform,
    }
    
    return render(request, 'social_app/post_content.html', context)
    
    

def comment_sent(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            image_file = request.FILES.get('image')
            if image_file:
                print(f"{image_file.name}")
                PostCommentImage.objects.create(post_comment=comment, image=image_file)
            
    return redirect('post_content', post_id=post_id)


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()
            
            if post.user != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
                    
            return func(request, post)
        return wrapper
    return inner_func


@like_toggle(Post)
def like_post(request, post):
    return render(request, 'social_app/likes.html', {'post': post})


@like_toggle(PostComment)
def like_comment(request, post):
    return render(request, 'social_app/likes_comment.html', {'comment': post})


def comment_delete(request, comment_id):
    comment = get_object_or_404(PostComment, pk=comment_id, user=request.user)
    post_id = comment.post.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post_content', post_id=post_id)
    
    referer_url = request.META.get('HTTP_REFERER', '/')
    
    return render(request, 'social_app/comment_delete.html', {'comment': comment, 'referer_url': referer_url})
    

    
def reply_sent(request, comment_id):
    comment = get_object_or_404(PostComment, pk=comment_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.parent_comment = comment
            reply.save()
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                reply_image = ReplyImage(reply=reply, image=image)
                reply_image.save()
            
    return redirect('post_content', comment.post.id)


def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id, user=request.user)
    post_id = reply.parent_comment.post.id
    
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted')
        return redirect('post_content', post_id=post_id)
    
    referer_url = request.META.get('HTTP_REFERER', '/')
    
    return render(request, 'social_app/reply_delete.html', {'reply': reply, 'referer_url': referer_url})
    
        

