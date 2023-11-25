from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.forms import RegisterForm


@login_required
def welcome(request):
    # Logic for the view goes here (if any)
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'registration.html', {'form': form})
