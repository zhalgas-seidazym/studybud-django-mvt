from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(email = email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {'page': page}
    return render(request, 'baseapp/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}
    return render(request, 'baseapp/login_register.html', context)

def home(request):
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        (
            Q(topic__name__icontains = q) |
            Q(name__icontains = q) |
            Q(description__icontains = q)
        ) &
        Q(approved = True) &
        Q(topic__approved = True)
    )

    topics = Topic.objects.filter(approved = True)[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(
        (
            Q(room__topic__name__icontains = q) |
            Q(room__description__icontains = q) |
            Q(room__name__icontains = q)
        ) &
        Q(room__approved = True) &
        Q(room__topic__approved = True)
    )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'baseapp/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk, approved = True)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'baseapp/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'baseapp/profile.html', context)

@login_required(login_url='login')
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
            approved = False,
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("Access Denied")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.approved = False
        room.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("Access Denied")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseapp/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("Access Denied")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'baseapp/delete.html', {'obj': message})

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'username' in post_data:
            post_data['username'] = post_data['username'].lower()
        form = UserForm(post_data, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk = user.id)

    context = {'form': form}
    return render(request, 'baseapp/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q', '')
    topics = Topic.objects.filter(name__icontains = q, approved = True)
    context = {'topics': topics}
    return render(request, 'baseapp/topics.html', context)

def activitiesPage(request):
    room_messages = Message.objects.filter(Q(room__approved = True))
    context = {'room_messages': room_messages}
    return render(request, 'baseapp/activity.html', context)

