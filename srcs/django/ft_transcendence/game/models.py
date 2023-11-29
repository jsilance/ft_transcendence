from django.db import models

# Create your models here.

SHAPE_CHOICES = (
	("1", "Spere"),
	("2", "Box"),
	("3", "Cylinder"),
)


class Shape(models.Model):
	type = models.CharField(max_length=1, choices=SHAPE_CHOICES)
	color = models.CharField(max_length=7, help_text='hex')

	def __str__(self):
		return str(self.id)

class ChatMessage(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
