from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score

@login_required(login_url='/accounts/login/')
def welcome(request):
	return render(request, 'welcome.html')

def leaderboard(request):
	users = Score.objects.all()
	return render(request, 'leaderboard.html', {'users': users})
