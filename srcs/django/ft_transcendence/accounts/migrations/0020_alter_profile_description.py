# Generated by Django 4.2.11 on 2024-03-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_profile_blocklist_alter_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Frostbitten Slayer: A frosty warrior wielding a frost axe, freezing enemies in their tracks.'),
        ),
    ]
