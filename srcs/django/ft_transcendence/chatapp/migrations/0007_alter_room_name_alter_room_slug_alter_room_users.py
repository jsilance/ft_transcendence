# Generated by Django 4.2.9 on 2024-02-06 14:26

import chatapp.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0006_alter_room_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(limit_choices_to={'is_active': True}, to=settings.AUTH_USER_MODEL),
        ),
    ]
