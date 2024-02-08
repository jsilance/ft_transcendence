from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.contrib.auth.models import User

# Create your views here.
@login_required
def chat_page(request):
    rooms = Room.objects.all()
    users = User.objects.all()
    return render(request, "chat.html", {
        "rooms": rooms,
        "users" : users
        })

def room(request, slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    context = {"slug":slug, "room_name":room_name, 'messages':messages}
    return render(request, "room.html", context)

def create_room(request):
    if request.method == "POST":
        # Assuming 'name' and 'slug' are provided in the form submission
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        user1 = request.user
        user2_id = request.POST.get('user2_id')
        user2 = User.objects.get(id=user2_id)

        existing_room = Room.objects.filter(user1=user1, user2=user2).exists()
        if not existing_room:
            # Create a new room
            room = Room.objects.create(name=name, slug=slug,user1=user1, user2=user2)
            return redirect('room', slug=slug)
        else:
            # Room already exists, redirect to the existing room
            room = Room.objects.get(user1=user1, user2=user2)
            return redirect('room', slug=room.slug)
