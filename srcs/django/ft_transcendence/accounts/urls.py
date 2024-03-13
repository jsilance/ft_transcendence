from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_v, name='signup'),
    path('blocking/', views.blocking, name='blocking'),
    path('login/', views.login_v, name='login'),
    path('callback/', views.callback, name='callback'),
    path('logout/', views.logout_v, name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
	path('profile/edit/', views.editprofile, name='profile_edit'),
    path('profile/<str:username>/delete/', views.deleteprofile, name='profile_delete'),
    path('friend_request/', views.send_friend_request, name='friend_request'),
    path('friend_remove/', views.remove_friend, name='remove_friend'),
    path('cancel_friend_request/', views.cancel_friend_request, name='friend_request_cancel'),
    path('accept_friend_request/<str:friend_request_id>', views.accept_friend_request, name='friend_request_accept'),
    path('decline_friend_request/<str:friend_request_id>', views.decline_friend_request, name='friend_request_decline'),
]