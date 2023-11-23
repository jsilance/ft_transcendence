from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def welcome(request):
    # Logic for the view goes here (if any)
    return render(request, 'welcome.html')

