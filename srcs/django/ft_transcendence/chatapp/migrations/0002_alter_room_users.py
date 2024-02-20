# Generated by Django 4.2.9 on 2024-02-06 13:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(limit_choices_to={'id__lt': 3}, to=settings.AUTH_USER_MODEL),
        ),
    ]