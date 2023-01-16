from django import forms
from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'article',
           'is_news',
           'text',
           'author',
           'category'
       ]



