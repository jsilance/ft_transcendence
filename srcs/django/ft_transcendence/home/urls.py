from django.urls import path
from home.views import welcome, register, profile, leaderboard, deleteprofile, editprofile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('', welcome, name='welcome'),
	path('profile/', profile, name='profile'),
	path('profile/<str:username>/delete/', deleteprofile, name='profile'),
	path('profile/edit/', editprofile, name='profile'),
    path('register/', register, name='register'),
	path('leaderboard/', leaderboard, name='leaderboard'),
]
