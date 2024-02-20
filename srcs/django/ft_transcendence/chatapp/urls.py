from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page),
    path('create_room/', views.create_room, name='create_room'),
    path('<str:slug>/', views.room, name='room'),
]