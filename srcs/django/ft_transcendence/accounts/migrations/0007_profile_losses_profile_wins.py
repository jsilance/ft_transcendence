# Generated by Django 4.2.10 on 2024-02-17 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
