# Generated by Django 4.2.10 on 2024-02-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Sure ,  here  is  a  description  of  a  fierce  warrior  for  a  video  game : \n\n Ra ze ,  a  battle - hard ened  warrior ,  wiel ds  her  powerful  Kat ana  with  unmatched  speed  and  strength .  With  her  swift  strikes  and  relentless  determination ,  she  commands  the  battlefield \n'),
        ),
    ]
