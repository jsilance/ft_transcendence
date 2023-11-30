from django.urls import path
from .views import websocket_test, game, lobby

urlpatterns = [
	path('', lobby, name='lobby'),
	path('<int:party_id>', game, name='game'),
    path('chatbox/<int:party_id>', websocket_test, name='websocket'),
]