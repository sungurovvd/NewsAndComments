from django import forms
from .models import Post, Author, Category

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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]

# class AuthorForm(forms.ModelForm):
#    class Meta:
#        model = Author
#        fields = [
#            'user'
#        ]


