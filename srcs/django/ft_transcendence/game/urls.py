from django.urls import path
from .views import websocket_test, game, lobby
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', lobby, name='lobby'),
	path('<int:party_id>', game, name='game'),
    path('chatbox/<int:party_id>', websocket_test, name='websocket'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
