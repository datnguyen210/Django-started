from pickle import FALSE
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import is_valid_path


# Create your views here.
from .models import Room, Topic
from .roomForm import RoomForm



def userLogin(req):
    page = 'login'
    if req.method == "POST":
        username = req.POST.get('username').lower()
        password = req.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(req, 'User not found!')
        user = authenticate(req, username = username, password = password)
        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "Incorrect password, please try again!")
    context ={'page': page}
    return render(req, 'base/login.html', context)

def userLogout(req):
    logout(req)
    return redirect('login')

def userRegister(req):
    form = UserCreationForm()
    if req.method == "POST":
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "Something went wrong!")
    context = {'form': form}
    return render(req, 'base/login.html', context)

def home(req):
    if req.user.is_authenticated:
        q = req.GET.get('q') if req.GET.get('q') != None else ''
        topics = Topic.objects.all()
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(host__username__icontains=q)| Q(description__icontains=q))
        context = {"rooms": rooms, 'topics': topics}
        return render(req, 'base/home.html', context)
    else:
        return redirect('login')
        

def room(req, id):
    if req.user.is_authenticated:
        room = Room.objects.get(id = id)
        context = {'room': room}
        return render(req, 'base/room.html', context)
    else:
        return redirect('login')
        

def createRoom(req):
    if req.user.is_authenticated:
        form = RoomForm()
        if(req.method == "POST"):
            form = RoomForm(req.POST)
            if(form.is_valid):
                form.save()
                return redirect('home')
        context = {"form": form}
        return render(req, 'base/create-room.html', context)
    else:
        return redirect('login')
        

def deleteRoom(req, id):
    user = req.user
    if user.is_authenticated:
        room = Room.objects.get(id = id)
        if room.host == user:
            if req.method == "POST":
                room.delete()
                return redirect('home')
            context = {"obj": room}
            return render(req, "base/delete-room.html", context)
        else:
            return HttpResponse('Not Your Room')
    else:
        return redirect('login')
        

def updateRoom(req,id):
    user = req.user
    if user.is_authenticated:
        room = Room.objects.get(id = id)
        if room.host == user:
            form = RoomForm(instance=room)
            if(req.method == "POST"):
                form = RoomForm(req.POST , instance=room)
                if(form.is_valid):
                    form.save()
                    return redirect('home')
            context = {"form": form}
            return render(req, "base/update-room.html", context)
        else: 
            return HttpResponse('Not Your Room')
            
    else: return redirect('login')
        
