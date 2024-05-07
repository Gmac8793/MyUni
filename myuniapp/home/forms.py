from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Place, Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='User Name')
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['password'].widget.attrs.update({'id': 'password'})
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), label='Email')
    username = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Name'}), label='User Name')
    password1 = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}), label='Password')
    password2 = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password Confirm'}), label='Confirm password')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['email'].widget.attrs.update({'id': 'email'})
        self.fields['password1'].widget.attrs.update({'id': 'password'})
        self.fields['password2'].widget.attrs.update({'id': 'confirm-password'})
        

        
class PlaceForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Place
        fields = ('name', 'detail', 'latitude', 'longitude')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'rounded-md p-2 border border-gray-300 focus:outline-none focus:border-indigo-500'})
        
        
class ProfileSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('bio', 'profileimg', 'location')
        

    
        
