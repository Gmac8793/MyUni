import auth_token
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib import messages
import json
from .forms import *
from .models import Place, Profile
from django.contrib.auth.decorators import login_required

#@login_required(login_url='/login/')
def home(request):
    places = Place.objects.all()
    places_data = [
        {
            'name': place.name,
            'id': place.id,
            'location': [place.latitude, place.longitude]
        }
        for place in places
    ]
    return render(request, 'home/home.html', {'places_data': json.dumps(places_data)})
   
def test(request):
    return render(request, 'home/test.html')
     
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
            #form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #Authenticate
            user = authenticate(username=username, password=password)
            login(request, user)
            #create profile
            Profile.objects.create(user=user, id_user=user.id)
            messages.success(request, "ลงทะเบียนสำเร็จ")
            return redirect('home')
    else:
        form = SignUpForm()          
    
    return render(request, 'home/signup.html', {'form':form})
    
#@login_required(login_url='/login/')
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_settings')
    else:
        form = ProfileSettingsForm(instance=request.user.profile)
    return render(request, 'home/profile_settings.html', {'form': form})

def add_new_place(request):
    if request.method == 'POST':
        form  = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PlaceForm()
    
    return render(request, 'home/add_new_place.html', {'form': form})


