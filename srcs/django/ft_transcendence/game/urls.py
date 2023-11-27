from django.urls import path
from .views import websocket_test

urlpatterns = [
	path('', websocket_test, name='game'),
]