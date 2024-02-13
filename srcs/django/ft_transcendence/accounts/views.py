from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest

authorize_uri = "https://api.intra.42.fr/oauth/authorize?\
	client_id=u-s4t2ud-c6b234d3edfab001ec93a17143651dcef4184d26390c68e82a5d64bd4ea6686e\
	&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fcallback%2F\
	&scope=public\
	&response_type=code\
	&state="

fromLogin = 'd56b699830e77ba53855679cb1d252da'
fromSignup = '7d2abf2d0fa7c3a0c13236910f30bc43'

def signup_v(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('home:welcome')
    else:
        form = UserCreationForm()
    return render(req, 'accounts/signup.html', {
        'form': form,
        'authorize_uri': authorize_uri+fromSignup
    })

def login_v(req):
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
    return render(req, 'accounts/login.html', {
        'form': form,
        'authorize_uri': authorize_uri+fromLogin,
        'known_users': User.objects.all(),
    })

"""
Callback function in case of login using Oauth2
- gets code
"""
def callback(req):
    if req.GET.get('code') is None:
        return HttpResponseBadRequest("Bad Request: Missing 'code' parameter")
    else:
        tmp_code = req.GET.get('code')
        return HttpResponse(f"<h1>The Temporary Code is: {tmp_code} </h1>")

def logout_v(req):
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