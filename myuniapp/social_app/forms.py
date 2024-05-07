from django import forms
from home.models import Post, Event, PostComment, Reply


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ('title', 'content',)
        
class CommentForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = PostComment
        fields = ['content', 'image']
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'w-full px-4 border border-2 border-transparent border-gray-200 focus:ring focus:ring-gray-500 focus:outline-none', 'placeholder': 'แสดงความคิดเห็น ...', 'rows': 5}), 
        }
        required=True
        labels = {
            'content': '',
            'image': 'Upload Image (optional)',
        }
        
class ReplyForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Reply
        fields = ['content', 'image']
        widgets = {
            'content' : forms.TextInput(attrs={'class': 'w-full  px-4 py-2  border border-2 border-transparent border-gray-200 focus:ring focus:ring-gray-500 focus:outline-none','placeholder': 'ตอบกลับ ...', 'class': "!text-sm"})
        }
        labels = {
            'content': '',
            'image': 'Upload Image',
        }
       
class EventForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Event
        fields = ('title', 'detail', 'start_date', 'end_date')