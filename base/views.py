from django.shortcuts import render, redirect
# Create your views here.
from .models import Room
from .roomForm import RoomForm

def home(req):
    rooms = Room.objects.all()
    context = {"rooms": rooms}
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