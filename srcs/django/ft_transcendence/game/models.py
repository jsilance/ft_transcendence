from django.db import models

# Create your models here.

SHAPE_CHOICES = (
	("1", "Border"),
	("2", "User"),
	("3", "Ball"),
)

class Shape(models.Model):
	party_id = models.CharField(max_length=7, help_text="id of the party", default=-1)
	item_id = models.CharField(max_length=7, help_text="id of the item", default=-1)
	type = models.CharField(max_length=1, choices=SHAPE_CHOICES)
	color = models.CharField(max_length=7, help_text='hex')
	posx = models.CharField(max_length=7, help_text='float position', default=0)
	posy = models.CharField(max_length=7, help_text='float position', default=0)

	def __str__(self):
		return str(self.party_id + " " + self.type + " " + self.item_id)

class MapSettings(models.Model):
	nbPlayer = models.CharField(max_length=3, help_text="number of users", default=2)
	listOfPlayer = models.CharField(help_text="list of player in json and if they are ready in json", default="")
	duringTime = models.CharField(help_text="time of the party", default=0)
	date = models.DateField(auto_now=True)

	def __str__(self):
		return str(self.id)

	def to_json(self):
		return {
            'id': self.id,
			'nbPlayer': self.nbPlayer,
			'duringTime': self.duringTime
		}
		# 'listOfPlayer': self.listOfPlayer,