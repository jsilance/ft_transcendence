# Import the path function and your WebSocket consumer
from django.urls import path
from .consumers import MyGameConsumer

websocket_urlpatterns = [
	path('ws/game/', MyGameConsumer.as_asgi()),
]
