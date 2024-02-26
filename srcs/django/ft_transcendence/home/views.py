from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score

@login_required(login_url='/accounts/login/')
def welcome(request):
	context = {
		"show_alert": True,
	}
	return render(request, 'welcome.html', context)

def leaderboard(request):
	context = {
		'all_users': User.objects.all(),
	}
	return render(request, 'leaderboard.html', context)
