from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score

@login_required(login_url='/accounts/login/')
def welcome(request):
	# Logic for the view goes here (if any)
	return render(request, 'welcome.html')

@login_required(login_url='/accounts/login/')
def profile(request):
	# Logic for the view goes here (if any)
	return render(request, 'profile.html')

def leaderboard(request):
	users = Score.objects.all()
	return render(request, 'leaderboard.html', {'users': users})
