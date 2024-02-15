from django.urls import path
from home.views import welcome, leaderboard
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
	path('', welcome, name='welcome'),
	path('leaderboard/', leaderboard, name='leaderboard'),
]