from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))#this creates the form for post
    
    class Meta:
        model = Post
        fields = {'content','image'}#in our form we have two form fields that is the content part and the image part

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Add a comment...'}))
    
    class Meta:
        model = Comment
        fields = {'body',}