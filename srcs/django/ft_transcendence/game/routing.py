# Import the path function and your WebSocket consumer
from django.urls import path
from .consumers import MyGameConsumer
from .consumers import PongConsumer

websocket_urlpatterns = [
    path('ws/chatbox/', MyGameConsumer.as_asgi()),
	path('ws/game/', PongConsumer.as_asgi())
]
