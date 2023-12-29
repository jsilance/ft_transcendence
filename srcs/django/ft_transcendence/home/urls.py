from django.urls import path
from home.views import welcome, leaderboard
from django.contrib.auth import views as auth_views

app_name = 'home'

urlpatterns = [
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	# path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('', welcome, name='welcome'),
    # path('register/', register, name='register'),
	path('leaderboard/', leaderboard, name='leaderboard'),
]