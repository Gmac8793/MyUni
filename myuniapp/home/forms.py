from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Place


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
        
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'latitude', 'longitude')
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    username = forms.CharField(label="", max_length=300, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

    
        
