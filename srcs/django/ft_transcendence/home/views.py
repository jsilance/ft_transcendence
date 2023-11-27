from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.forms import RegisterForm
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score

@login_required
def welcome(request):
	# Logic for the view goes here (if any)
	return render(request, 'welcome.html')

@login_required
def profile(request):
	# Logic for the view goes here (if any)
	return render(request, 'profile.html')

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')  # Redirect to login page after successful registration
	else:
		form = RegisterForm()
	return render(request, 'registration.html', {'form': form})

def leaderboard(request):
	users = Score.objects.all()
	return render(request, 'leaderboard.html', {'users': users})

@login_required
def deleteprofile(request, username):
	User.objects.delete(username)
	return redirect('login')

@login_required
def editprofile(request):
	return render(request, 'editprofile.html')