from django.db import models

# Create your models here.

SHAPE_CHOICES = (
	("1", "Border"),
	("2", "User"),
	("3", "Ball"),
)

class MapSettings(models.Model):
	listOfPlayer = models.CharField(help_text="list of player in json and if they are ready in json", default="")
	duringTime = models.CharField(help_text="time of the party", default=0)
	date = models.DateField(auto_now=True)

	def __str__(self):
		return str(self.id)

	def to_json(self):
		return {
			'id': self.id,
			'duringTime': self.duringTime
		}
		# 'listOfPlayer': self.listOfPlayer,

	def delete(self, *args, **kwargs):
		super(MapSettings, self).delete(*args, **kwargs)