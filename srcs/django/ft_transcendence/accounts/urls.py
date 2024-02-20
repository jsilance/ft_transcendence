from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_v, name='signup'),
    path('login/', views.login_v, name='login'),
    path('callback/', views.callback, name='callback'),
    path('logout/', views.logout_v, name='logout'),
    path('profile/', views.profile, name='profile'),
	path('profile/edit/', views.editprofile, name='profile_edit'),
    path('profile/<str:username>/delete/', views.deleteprofile, name='profile_delete'),
]