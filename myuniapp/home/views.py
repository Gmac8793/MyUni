from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Count
import json

from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    places = Place.objects.all()
    places_data = []
    for place in places:
        place_images = place.images.all()
        image_urls = [image.image.url for image in place_images]
        
        events_ongoing = Event.objects.filter(place=place, end_date__gte=timezone.now())
        events_ongoing_data = []
        
        for event in events_ongoing:
            event_data = {
                'title': event.title,
                'detail': event.detail,
                'start_date': event.start_date.strftime('%m/%d/%Y, %H:%M:%S'),
                'end_date': event.end_date.strftime('%m/%d/%Y, %H:%M:%S'),
            }
            events_ongoing_data.append(event_data)
            
        place_data = {
            'name': place.name,
            'detail': place.detail,
            'id': place.id,
            'location': [place.latitude, place.longitude],
            'image_urls': image_urls,
            'events_ongoing': events_ongoing_data
        }
        places_data.append(place_data)  
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None 
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count() if request.user.is_authenticated else 0
          
    return render(request, 'home/home.html', {
        'places_data': json.dumps(places_data), 
        'profile': profile,
        'unread_notifications_count': unread_notifications_count
    })
   
     
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "ยินดีต้อนรับเข้าสู่หน้าหลัก!")
                return redirect('home')
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาเข้าสู่ระบบใหม่อีกครั้ง")   
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})
        

def logout_user(request):
    logout(request)
    messages.success(request, "คุณได้ออกจากระบบแล้ว")
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #create profile
            Profile.objects.create(user=user)
            messages.success(request, "ลงทะเบียนสำเร็จ")
            return redirect('home')
    else:
        form = SignUpForm()          
    
    return render(request, 'home/signup.html', {'form':form})

def profile(request, username):
    profile = []
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user__username=username)
        user_posts = Post.objects.filter(user=profile.user)
        
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            # follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
                
                Notification.objects.create(
                    user=profile.user,
                    message=f"{request.user.username} has followed you"
                )
            current_user_profile.save()   
    else: 
        user_posts = []
        
    follower_count = profile.followed_by.count()
    following_count = profile.follows.count()
    context = {
        'profile': profile,
        'user_posts': user_posts, 
        'follower_count': follower_count,
        'following_count': following_count,
           
    }
    return render(request, 'home/profile.html', context)



            
            
    
#@login_required(login_url='/login/')
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.profile.user.username
            return redirect(reverse('profile', kwargs={'username': username}))
    else:
        form = ProfileSettingsForm(instance=request.user.profile)
        
    referer_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'home/profile_settings.html', {'form': form, 'referer_url': referer_url})

def add_new_place(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    
    if request.method == 'POST':
        form  = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.latitude = lat
            place.longitude = lng
            place.save()
            if 'image' in request.FILES:
                place_image = PlaceImage(place=place, image=request.FILES['image'])
                place_image.save()
            return redirect('home')
    else:
        place_url = {'latitude': lat, 'longitude': lng}
        form = PlaceForm(initial=place_url)
    
    return render(request, 'home/add_new_place.html', {'form': form})


