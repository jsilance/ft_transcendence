# Generated by Django 4.2.10 on 2024-02-08 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0009_room_test1_room_test2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='test1',
        ),
        migrations.RemoveField(
            model_name='room',
            name='test2',
        ),
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
        migrations.AddField(
            model_name='room',
            name='user1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='room_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='user2',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='room_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]