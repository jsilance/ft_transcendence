from django.urls import path
from .views import websocket_test, game

urlpatterns = [
	path('', game, name='game'),
    path('chatbox/', websocket_test, name='websocket'),
]