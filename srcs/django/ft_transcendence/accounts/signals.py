from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# automatically create profile when new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # prevents access of Profile before it has been associated
    # with the User model, which leads to AttributeError
    if hasattr(instance, 'profile'):
        instance.profile.save()