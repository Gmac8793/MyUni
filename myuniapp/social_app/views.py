from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from social_app.utils import comment_notification, reply_notification
from social_app.forms import *
from django.db.models import Count
import json
from django.views import generic
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
            Notification.objects.create(user=request.user, message=f'New post created: {post.title}')
            
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
        Notification.objects.create(user=request.user, message=f'New event created: {event.title}')
        
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

#Events Calendar
def event_calendar(request):
    all_events = Event.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'social_app/event_calendar.html', context)

def all_events(request):
    all_events = Event.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.title,
            'id': event.id,
            'start': event.start_date.strftime("%Y-%m-%dT%H:%M:%S") if event.start_date else None,
            'end': event.end_date.strftime("%Y-%m-%dT%H:%M:%S") if event.end_date else None,
        })
    return JsonResponse(out, safe=False)


# def add_event(request):
#     start_date = request.GET.get("start", None)
#     end_date = request.GET.get("end", None)
#     title = request.GET.get("title", None)
   
#     event = Event(name=str(title), start=start_date, end=end_date)
#     event.save()
#     data = {}
#     return JsonResponse(data)
  
  
def event_from_calendar(request):
    if request.method == 'POST':
        form = EventCalendarForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            if 'event_image' in request.FILES:
                event_image = EventImage(event=event, image=request.FILES['event_image'])
                event_image.save()
                
                
                
            Notification.objects.create(user=request.user, message=f'New event added from calendar: {event.title}')
            
            return redirect('event_calendar')
    else:
        form = EventCalendarForm()     
    referer_url = request.META.get('HTTP_REFERER', '/') 
    return render(request, 'social_app/event_from_calendar.html', {'form': form, 'referer_url': referer_url})
 
def event_details(request, pk):
    event = Event.objects.get(id=pk)
    profile = request.user.profile
    eventmember = EventMember.objects.filter(event=event)
    
    context = {
        'event': event,
        'profile': profile,
        'eventmember': eventmember,
    }
    return render(request, 'social_app/event_details.html', context)


def add_event_member(request, event_id):
    form = AddMemberForm()
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = EventMember.objects.filter(event=event_id)
            if member.count() <= 9:
                member = form.cleaned_data['member']
                EventMember.objects.create(event=event, member=member)
                
                Notification.objects.create(user=member, message=f'You have been added to the event "{event.title}"')
                return redirect('event_calendar')
            else:
                print("----------Member limit exceed!----------")
    
    referer_url = request.META.get('HTTP_REFERER', '/')
    context = {
        'form': form,
        'event': event,
        'referer_url': referer_url,
    }
    return render(request, 'social_app/add_member.html', context)


def remove_member(request, event_id, member_id):
    event = get_object_or_404(Event, id=event_id)
    member = get_object_or_404(EventMember, event=event, member_id=member_id)
    
    if request.user == event.user:
        member.delete()
    return redirect('event_details', pk=event_id)

def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted')
        return redirect('event_calendar')
    
    referer_url = request.META.get('HTTP_REFERER', '/')
    
    return render(request, 'social_app/event_delete.html', {'event': event, 'referer_url': referer_url})

def event_edit(request, pk):
    event = get_object_or_404(Event, id=pk)
    if request.method == 'POST':
        form = EventCalendarForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            if 'image' in request.FILES:
                event_image = EventImage(event=event, image=request.FILES['image'])
                event_image.save()
            return redirect('event_details', pk=event.pk)
    else:
        form = EventCalendarForm(instance=event)
        
    referer_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'social_app/event_edit.html', {'form': form, 'event': event, 'referer_url': referer_url,})

        
@login_required(login_url='/login/')
def feed(request):
    place_id = request.GET.get('id')
    place = get_object_or_404(Place, id=place_id)
    posts = Post.objects.filter(place=place)
    profile = request.user.profile
    
    events = Event.objects.filter(place=place, end_date__gte=timezone.now())
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count() if request.user.is_authenticated else 0

    referer_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'social_app/feed.html', {
        'place': place, 
        'posts': posts, 
        'events': events, 
        'profile': profile,
        'unread_notifications_count': unread_notifications_count,
        'referer_url': referer_url,
    })


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
    replyform = ReplyForm(request.FILES)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
                
            comment_notification(request.user, post, comment)
                
    context = {
        'comment': comment, 
        'post': post, 
        'replyform': replyform
    }
            
    return render(request, 'social_app/add_comment.html', context)


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
                    
                Notification.objects.create(user=post.user, message=f'{request.user.username} liked your {model.__name__.lower()}')
                    
            return func(request, post)
        return wrapper
    return inner_func
 

@like_toggle(Post)
def like_post(request, post):
    return render(request, 'social_app/likes.html', {'post': post})


@like_toggle(PostComment)
def like_comment(request, post):
    return render(request, 'social_app/likes_comment.html', {'comment': post})


@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'social_app/likes_reply.html', {'reply': post})


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
    replyform = ReplyForm(request.FILES)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.parent_comment = comment
            reply.save()
        
            reply_notification(request.user, comment, reply)
                
    context = {
        'comment': comment, 
        'reply': reply, 
        'replyform': replyform
    }
            
    return render(request, 'social_app/add_reply.html', context)


def reply_form(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    replyform = NestedReplyForm()
    reply_nested = None
    
    if request.method == 'POST':
        form = NestedReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply_nested = form.save(commit=False)
            reply_nested.user = request.user
            reply_nested.parent_reply = reply
            reply_nested.level = reply.level + 1
            reply_nested.save()
            
            return render(request, 'social_app/reply.html', {'reply': reply_nested})
    
    context = {
        'reply': reply,
        'replyform': replyform,
    }
    
    return render(request, 'social_app/add_replyform.html', context)


def reply_delete(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id, user=request.user)
    reply.delete()
    return HttpResponse('')


def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    referer_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'social_app/notifications.html', {
        'notifications': user_notifications,
        'referer_url': referer_url,
    })

def mark_notifications_as_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications')
    
    
    

