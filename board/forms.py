from django import forms 
from .models import Post

class PostSearchForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ['title']

