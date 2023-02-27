from django import forms
from django.forms import ModelForm
from .models import Blog, Blogimages

class blogviewform(ModelForm):
    class Meta:
        model= Blog
        fields=['title','description','author']         


class createblogpostform(ModelForm):
    class Meta:
        model=Blog
        fields=['title','thumbnail']
