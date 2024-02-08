from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField()
    slug = models.SlugField()
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_user1', default=1)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_user2', default=2)

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)