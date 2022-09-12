from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
from .models import Room, Topic
from .roomForm import RoomForm

def home(req):
    q = req.GET.get('q') if req.GET.get('q') != None else ''
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(host__username__icontains=q)| Q(description__icontains=q))
    context = {"rooms": rooms, 'topics': topics}
    return render(req, 'base/home.html', context)


def room(req, id):
    room = Room.objects.get(id = id)
    context = {'room': room}
    return render(req, 'base/room.html', context)

def createRoom(req):
    form = RoomForm()
    if(req.method == "POST"):
        form = RoomForm(req.POST)
        if(form.is_valid):
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(req, 'base/create-room.html', context)

def deleteRoom(req, id):
    room = Room.objects.get(id = id)
    if(req.method == "POST"):
        room.delete()
        return redirect('home')
    context = {"obj": room}
    return render(req, "base/delete-room.html", context)

def updateRoom(req,id):
    room = Room.objects.get(id = id)
    form = RoomForm(instance=room)
    if(req.method == "POST"):
        form = RoomForm(req.POST , instance=room)
        if(form.is_valid):
            form.save()
            return redirect('home')
    context = {"form": form}
    return render(req, "base/update-room.html", context)