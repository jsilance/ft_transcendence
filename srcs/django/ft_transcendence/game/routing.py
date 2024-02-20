# Import the path function and your WebSocket consumer
from django.urls import re_path
from .consumers import MyGameConsumer
from .consumers import PongConsumer

websocket_urlpatterns = [
    re_path('ws/chatbox/', MyGameConsumer.as_asgi()),
	re_path('ws/game/', PongConsumer.as_asgi())
]