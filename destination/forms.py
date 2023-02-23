
from django import forms
from .models import Comment,Place_rating 

class comment_form(forms.ModelForm):
    class Meta:
        model=Comment 
        fields=['comment_body']

rate_choices=[(1,1),(2,2),(3,3),(4,4),(5,5)]

class rateform(forms.ModelForm):
    Choice=[
        (1,1),
           (2,2),
        (3,3),
           (4,4),
         (5,5)]
    rate=forms.ChoiceField(choices=Choice,widget=forms.RadioSelect)
    class Meta:
        model=Place_rating
        fields=['rate']