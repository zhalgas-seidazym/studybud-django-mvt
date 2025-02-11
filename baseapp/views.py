from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms = [
#     {
#         'id': 1,
#         'name': 'Lets learn django!'
#     },
#     {
#         'id': 2,
#         'name': 'Lets learn frontend!'
#     },
#     {
#         'id': 3,
#         'name': 'Lets learn python!'
#     },
# ]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'baseapp/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    print(room)
    context = {'room': room}
    return render(request, 'baseapp/room.html', context)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'baseapp/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseapp/delete.html', {'obj': room})

