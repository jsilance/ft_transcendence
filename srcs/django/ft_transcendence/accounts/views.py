from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
import requests
from dotenv import load_dotenv
import os

# get acces to environment variables
load_dotenv()

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
Callback for Oauth2 logic
--
catches tmp_code, exchanges it for an access token, use that
token to get user informations
"""
def callback(req):
    temporary_code = req.GET.get('code')
    if temporary_code is None:
        return HttpResponseBadRequest("Bad Request: Missing 'code' parameter")

    o42 = oauth42()
    token = o42.get_token(temporary_code)
    data = o42.get_user_data(token)
    intra_login = data.get('login')

    if intra_login in str(User.objects.all()):
        user = User.objects.get(username=intra_login)
        login(req, user)
        if 'next' in req.POST:
            return redirect(req.POST.get('next'))
        else:
            return redirect('home:welcome')
    else:
        return redirect('accounts:login')

class oauth42:
    # exchange temporary code for access token
    def get_token(self, code):
        url = 'https://api.intra.42.fr/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'code': code,
            'redirect_uri': 'http://localhost:8000/accounts/callback/' # YOU..AAARG!
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            # Handle error
            return response

    # use access token to access user data
    def get_user_data(self, access_token):
        # Make a request to the provider's API to get user information
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            return None


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