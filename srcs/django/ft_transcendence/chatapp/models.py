from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    user1 = models.OneToOneField(User, related_name='user1', on_delete=models.CASCADE)
    user2 = models.OneToOneField(User, related_name='user2', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)