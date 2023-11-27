from django.db import models

class Score(models.Model):
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	score = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username + " " + str(self.score) + " " + str(self.date)