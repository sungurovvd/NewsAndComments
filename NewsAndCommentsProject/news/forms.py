from django import forms
from .models import Post, Author

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

# class AuthorForm(forms.ModelForm):
#    class Meta:
#        model = Author
#        fields = [
#            'user'
#        ]


