# from django.shortcuts import render

# # Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q #search
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, User
# from .forms import RoomForm, UserForm, MyUserCreationForm
# from django.views import generic
# from django.utils.decorators import method_decorator
from .models import Room
from .forms import RoomForm, UserForm

# rooms = [
#     {'id':1, 'name':'Shivapuri Trekking!'},
#     {'id':2, 'name':'Pashupati Darshan'},
#     {'id':3, 'name':'Kathmandu Durbarsquare Visit'},
# ] 


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('index')

    # if request.method == 'POST':
    #     email = request.POST.get('email').lower()
    #     password = request.POST.get('password')

    #     try:
    #         user = User.objects.get(email = email)
    #     except:
    #         messages.error(request,'User does not exist')

    #     user = authenticate(request, email = email, password = password)

    #     if user is not None:
    #         login(request,user)
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'Email OR Password does not match')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Email OR Password does not match')

        
    context = {'page': page}
    return render(request,'chatbox/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def registerPage(request):
    form = UserCreationForm()
    # page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username =user.username.lower()
            user.save()
            login(request, user)
            return redirect ('index')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request,'chatbox/login_register.html', {'form': form})


# def home(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ""

#     rooms = Room.objects.filter(
#         Q(topic__name__icontains=q) |
#         Q(name__icontains=q) |
#         Q(description__icontains=q)
#     )

#     topics = Topic.objects.all()[0:5]
#     room_count =rooms.count()
#     room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

#     context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
#     return render(request, 'base/home.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    topics = Topic.objects.all()[0:5]
    room_count =rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))


    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'chatbox/home.html', context )


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'chatbox/home.html', context )


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')

    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'chatbox/room.html', context)
            

# @login_required(login_url = 'login')
# def room(request,pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all().order_by('created')
#     participants = room.participants.all()

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user = request.user,
#             room = room,
#             body = request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect ('room', pk=room.id)

#     context = {'room': room,'room_messages': room_messages, 'participants':participants}
#     return render(request, 'base/room.html',context)


@login_required(login_url = 'login')
def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages,'topics':topics}
    return render(request, 'chatbox/profile.html', context)


# @login_required(login_url = 'login')
# def createRoom(request):
#     form = RoomForm()
#     topics = Topic.objects.all()

#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name = topic_name)

#         Room.objects.create(
#             host = request.user,
#             topic = topic,
#             name = request.POST.get('name'),
#             description = request.POST.get('description'),
#         )
#         return redirect('home')

#     context={'form':form, 'topics':topics}
#     return render(request, 'base/room_form.html',context)


@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('index')
    context={'form': form, 'topics':topics}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
        # print(request.POST)
    context={'form': form}
    return render(request, 'chatbox/room_form.html', context)


# @login_required(login_url = 'login')
# def updateRoom(request,pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance = room)
#     topics = Topic.objects.all()

#     if request.user != room.host:
#         return HttpResponse('You are not allowed to update this room!')

#     if request.method == "POST":
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name = topic_name)

#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')


#     context= {'form':form, 'topics':topics, 'room':room}
#     return render(request,"base/room_form.html", context)

@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('index')
        

    context = { 'form' : form, 'topics':topics, 'room':room }
    return render(request,"chatbox/room_form.html", context)


# @login_required(login_url = 'login')
# def deleteRoom(request,pk):
#     room = Room.objects.get(id=pk)

#     if request.user != room.host:
#         return HttpResponse('You are not allowed to delete this room!')

#     if request.method == 'POST':
#         room.delete()
#         return redirect ('home')

#     return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url = 'login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room!')
    
    if request.method == 'POST':
        room.delete()
        return redirect ('index')
    
    return render(request, 'chatbox/delete.html', {'obj':room})



@login_required(login_url = 'login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You cannot delete this message!')

    if request.method == 'POST':
        message.delete()
        return redirect ('home')

    return render(request, 'chatbox/delete.html', {'obj':message})





@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'chatbox/update-user.html', {'form': form})


# def topicsPage(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ""
#     topics = Topic.objects.filter(name__icontains=q)
#     return render(request, 'base/topics.html',{'topics':topics})


# def activityPage(request):
#     room_messages = Message.objects.all()
#     return render(request, 'base/activity.html',{'room_messages':room_messages})