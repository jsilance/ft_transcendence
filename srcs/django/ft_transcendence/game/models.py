from django.db import models

# Create your models here.

SHAPE_CHOICES = (
	("1", "Border"),
	("2", "User"),
	("3", "Ball"),
)

class Shape(models.Model):
	type = models.CharField(max_length=1, choices=SHAPE_CHOICES)
	color = models.CharField(max_length=7, help_text='hex')
	posx = models.CharField(max_length=7, help_text='float position', default=0)
	posy = models.CharField(max_length=7, help_text='float position', default=0)

	def __str__(self):
		return str(self.type)

class MapSettings(models.Model):
	nbPlayer = models.CharField(max_length=3, help_text="number of users")
	listOfPlayer = models.CharField(help_text="list of player in json and if they are ready in json")
	duringTime = models.CharField(help_text="time of the party", default=0)
	date = models.DateField(auto_now=True)

	def __str__(self):
		return str(self.id)