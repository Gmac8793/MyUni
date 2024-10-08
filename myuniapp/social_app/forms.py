from django import forms
from home.models import Post, Event, PostComment, Reply, Place, EventMember


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ('title', 'content',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'w-full px-4 text-sm border border-2 border-transparent border-gray-200 focus:ring focus:ring-black focus:outline-none', 'placeholder': 'แสดงความคิดเห็น ...', 'rows': 5}), 
        }
        required=True
        labels = {
            'content': '',
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'class': 'w-full px-4 py-2 text-xs border border-2 border-transparent border-gray-200 focus:ring focus:ring-black focus:outline-none','placeholder': 'ตอบกลับ ...'})
        }
        labels = {
            'content': '',
        }
   
   
class NestedReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'autofocuss': True, 'class': '!text-xs bg-gray-200 !p-0 !pl-0 !h-8','placeholder': 'ตอบกลับ ...', 'class': "!text-xs"})
        }
        labels = {
            'content': '',
        }     
        
     
class EventForm(forms.ModelForm):
    #image = forms.ImageField(required=False)
    class Meta:
        model = Event
        fields = ('title', 'detail', 'start_date', 'end_date')
        

class EventCalendarForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Event
        fields = ('title', 'detail', 'image', 'start_date', 'end_date', 'place')
        
        
    def __init__(self, *args, **kwargs):
        super(EventCalendarForm, self).__init__(*args, **kwargs)
        self.fields['place'].queryset = Place.objects.all()
        
        
class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["member"]