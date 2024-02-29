from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt

def landingPage(request):
    """ Delivers the landing page with a few stories"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:9]
    topics = Topic.objects.all()[0:6]
    subjects_count = topics.count()
    room_count = rooms.count()
    context = {'subjects_count': subjects_count, "rooms": rooms, "topics": topics, "room_messages": room_messages,
               'room_count': room_count}
    return render(request, 'landing_page.html', context)

# Login page
@csrf_exempt
def loginPage(request):
    """ View to handle logging of a user """
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password Does not Exist")

    context = {'page': page}
    return render(request, 'login_register.html', context)

@csrf_exempt
@login_required(login_url='login')
def user_profile(request, pk):
    """ Function to preview the profile of a user """
    # user = get_user_model()
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'topics': topics, 'user': user, 'rooms': rooms,
               'room_messages': room_messages}
    return render(request, 'user_profile.html', context)

@csrf_exempt
@login_required(login_url='login')
def update_profile(request):
    """ Handles editing of the users details """
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'update_user_profile.html', context)


def logoutuser(request):
    """ Handles users getting out of sessions """
    logout(request)
    return redirect('home')

@csrf_exempt
def register_user(request):
    """ Handles registrations of new users """
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # to access the user right away.
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {"form": form}
    return render(request, 'signup.html', context)


@login_required(login_url='login')
def home(request):
    """ Handles everything that is show on the home page"""
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:9]
    topics = Topic.objects.all()[0:6]
    subjects_count = topics.count()
    room_count = rooms.count()
    context = {'subjects_count': subjects_count, "rooms": rooms, "topics": topics, "room_messages": room_messages,
               'room_count': room_count}
    return render(request, 'home.html', context)


# Rooms start
@login_required(login_url='login')
def room(request, pk):
    """ Handles everything to do with the Story telling room """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    topics = Topic.objects.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {"topics": topics, "room": room, "room_messages": room_messages,
               "participants": participants}
    return render(request, 'room.html', context)


@login_required(login_url='login')
def reading_time(request, pk):
    """ Delivers a page dedicated to just reading the story """
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    topics = Topic.objects.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {"topics": topics, "room": room, "room_messages": room_messages,
               "participants": participants}
    return render(request, 'reading_time.html', context)


@csrf_exempt
@login_required(login_url="login")
def createRoom(request):
    """ Helps tpo create a new room to start telling stories """
    topics = Topic.objects.all()
    form = RoomForm()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)

@csrf_exempt
@login_required(login_url="login")
def updateRoom(request, pk):
    """ Helps to edit a story by either the host or a collaborator """
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        if request.method == "POST":
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            Room.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description')
            )
            return redirect('home')
        context = {'form': form, 'topics': topics}
        return render(request, 'room_form.html', context)
        

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')
    context = {'topics': topics, 'form': form, 'room': room}
    return render(request, 'room_form.html', context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    """ Deletes a story room incase it isnt needed anymore """
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You arent allowed in here")

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'delete.html', context)
# Rooms end


# Messages start
@login_required(login_url='login')
def message(request, pk):
    """ Creates the a new comment/message"""
    message = Message.objects.get(id=pk)
    context = {'message': message}
    return render(request, 'message.html', context)


@login_required(login_url="login")
def delete_message(request, pk):
    """ Deletes a created comment/message """
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You arent allowed in here")

    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': message})


@login_required(login_url='login')
def update_message(request, pk):
    """ Helps to edit the message/comment by the writer """
    message = Message.objects.get(id=pk)
    form = MessageForm(instance=message)

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid:
            form.save()
            return redirect('room')
    context = {"form": form}
    return render(request, 'message_form.html', context)

# messages end


# topics
@login_required(login_url='login')
def topics(request):
    """ Handdles all topics or genres """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    subjects_count = topics.count()
    context = {'topics': topics, 'subjects_count': subjects_count}
    return render(request, 'topics.html', context)


# activities
@login_required(login_url='login')
def activities(request):
    """ Handles the notoifications part of the applications """
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'activity.html', context)
