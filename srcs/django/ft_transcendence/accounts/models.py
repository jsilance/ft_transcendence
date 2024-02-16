from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.svg', upload_to='profile_pics')
    isstudent = models.BooleanField(default=False)
    friends = ArrayField(models.CharField(max_length=30), null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'