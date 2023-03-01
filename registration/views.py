
from email import message
from django.shortcuts import render,redirect
from .forms import preferenceform, profileform, UsercreateForm, userupdateform
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.views.generic import CreateView
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from registration.models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def profile_editpage(request):
    if request.method=="POST":
      
        user_form= userupdateform(request.POST,instance=request.user)
        profile_form=profileform(request.POST,request.FILES,instance=request.user.profile)
        
        img =  request.FILES.get('pp')
        
        if user_form.is_valid() and profile_form.is_valid():
            
            if img is not None:
                post = Profile.objects.get(user=request.user)
                post.profile_pic = img 
                post.save()
            user_form.save()
            profile_form.save() 
            
            return redirect('profilepage')
    else:
        user_form=userupdateform(instance=request.user)
        profile_form=profileform(instance=request.user.profile)
        
    return render(request,'editprofile.html', {'form':user_form,'p_form':profile_form}) 

@login_required 
def accountsetting(request):
    if request.method=="POST":
        form=userupdateform(request.POST,instance=request.user, prefix = 'form')
        profile_form=profileform(request.POST,request.FILES, prefix = 'profile_form')
        preference_form=preferenceform(request.POST, prefix = 'preference_form')
        
        if form.is_valid() and profile_form.is_valid() and preference_form.is_valid():
            form.save()

            pf = profile_form.save(commit=False)
            pf.user = request.user
            pref = preference_form.save(commit=False)
            pref.user = request.user
            pf.save()
            pref.save()  
            return redirect('placelist')
            
    else:
        form=userupdateform(instance=request.user, prefix = 'form')
        profile_form=profileform(prefix = 'profile_form')
        preference_form=preferenceform(prefix = 'preference_form')
    return render(request, 'preferencesinfo.html',{'f':form,'p':profile_form,'pr':preference_form})    


def registerpage(request):
    if request.method=="POST":
        user_form=UsercreateForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            u_name = user_form.cleaned_data.get('username')
            messages.success(request,f'Account created successfully for {u_name} !!')
            return redirect('login')
    else:
        user_form=UsercreateForm()       
    return render(request,'registeruser.html',{'form':user_form})        

