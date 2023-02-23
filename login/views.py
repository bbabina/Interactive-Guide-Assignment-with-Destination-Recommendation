from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from .forms import loginform
from registration.models import Profile 
from django.contrib import messages
# Create your views here.

def loginpage(request):
    if request.method=="POST":
        #check either user exist or not
        login_form=loginform(request.POST)
        if login_form.is_valid():
             un=login_form.cleaned_data.get('username')
             pwd=login_form.cleaned_data.get('password')
             thisuser=authenticate(request,username=un,password=pwd)
             if thisuser is not None:
                if Profile.objects.filter(user=thisuser).exists():
                    login(request,thisuser)
                    return redirect('placelist')
                else:
                    login(request,thisuser)
                    return redirect('as')
             else:
                 messages.error(request,f'either username or password is invalid!!')


    else:
        login_form=loginform()
    return render(request,'login.html',{'form':login_form})

def logoutpage(request):
      logout(request)
      return redirect('login')



    

    

