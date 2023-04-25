from django.forms import ModelForm, widgets 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Preferences
from destination.models import Places

class UsercreateForm(UserCreationForm):
    
    class Meta:
        model= User
        fields= ['username','email','password1','password2']


class profileform(ModelForm):
    place = forms.ModelChoiceField(queryset=Places.objects.all(), widget=forms.Select, required=False)
    class Meta:
        model= Profile
        fields= ['middle_name','sex','age','phone_number','nationality','profile_pic','is_guide','place']
        labels={
            'is_guide': 'Become a guide',
            'place':'Select destination'
        }
        
class userupdateform(ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model= User
        fields= ['email','first_name','last_name']
      

class preferenceform(forms.ModelForm):
    
    culture=forms.BooleanField(required=False)
    adventure=forms.BooleanField(required=False)
    wildlife=forms.BooleanField(required=False)
    sightseeing=forms.BooleanField(required=False)
    history=forms.BooleanField(required=False)
    religious=forms.BooleanField(required=False)
    child_friendly=forms.BooleanField(required=False)
    class Meta:
        model= Preferences
        fields = ['culture','adventure','wildlife','sightseeing','history','religious','child_friendly']
    