from django.shortcuts import render, redirect
from user.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()

    return render(request, 'registration/registration.html', {'form': form})
