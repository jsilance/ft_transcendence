from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def signup_view(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('home:welcome')
    else:
        form = UserCreationForm()
    return render(req, 'accounts/signup.html', {'form': form})

def login_view(req):
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            user = form.get_user()
            login(req, user)
            if 'next' in req.POST:
                return redirect(req.POST.get('next'))
            else:
                return redirect('home:welcome')
    else:
        form = AuthenticationForm()
    return render(req, 'accounts/login.html', {'form': form})

def logout_view(req):
    if req.method == 'POST':
        logout(req)
        return redirect('home:welcome')

################################################################################

@login_required(login_url='/accounts/login/')
def profile(request):
     return render(request, 'accounts/profile.html')

@login_required(login_url='/accounts/login/')
def deleteprofile(request, username):
    # Ensure the user is deleting their own profile or is a superuser
    if request.user.username != username and not request.user.is_superuser:
        return render(request, '404.html')

    # Retrieve the user instance
    try:
        user_to_delete = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, '500.html', {'message': 'User not found'})
    
    # Delete the user instance
    user_to_delete.delete()
    return redirect('accounts:login')

@login_required(login_url='/accounts/login/')
def editprofile(request):
	return render(request, 'accounts/editprofile.html')