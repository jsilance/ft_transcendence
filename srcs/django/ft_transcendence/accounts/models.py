from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from PIL import Image
from django.conf import settings
from django.utils import timezone
from .helpers import pick_random_description

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    isstudent = models.BooleanField(default=False)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    description = models.CharField(default=pick_random_description())
    blocklist = models.ManyToManyField(User, blank=True, related_name="blocklist")

    def __str__(self):
        return f'{self.user.username} Profile'
    
    # resizes all large profile images
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username
    
    def add_friend(self, account):
        """
        Add a new friend
        """
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        """
        Remove friend
        """
        if account in self.friends.all():
            self.friends.remove(account)
    
    def unfriend(self, target):
        """
        Unfriend someone
        """
        my_friends_list = self # person terminating 
        my_friends_list.remove_friend(target)

        targets_friends_list = FriendList.objects.get(user=target)
        targets_friends_list.remove_friend(self.user)

    def is_mutual_friend(self, target):
        """
        Is this a friend
        """
        if target in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
        1. SENDER:
            - Person sending the friend request
        2. RECEIVER:
            - Person receiving the friend request
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        """
        Accept a friend request
            Update both SENDER and RECEIVER friend lists
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()
    
    def decline(self):
        """
        Decline a friend request (sent to you)
            Is it "declined" by setting the "is_active" field to False
        """
        self.is_active = False
        self.save()
    
    def cancel(self):
        """
        Cancel a friend request (you sent)
            It is "cancelled" by setting the "is_active" field to False
        """
        self.is_active = False
        self.save()