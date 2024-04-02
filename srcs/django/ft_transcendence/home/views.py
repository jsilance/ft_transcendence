from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Score
from django.http import HttpResponse
from render_block import render_block_to_string

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
	if 'HTTP_HX_REQUEST' in request.META:
		html = render_block_to_string('leaderboard.html', 'body', context)
		return HttpResponse(html)
	return render(request, 'leaderboard.html', context)
