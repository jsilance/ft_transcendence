from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import FriendList

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
import requests
from dotenv import load_dotenv
import os
from django.conf import settings

# get acces to environment variables
load_dotenv()

authorize_uri = "https://api.intra.42.fr/oauth/authorize?\
	client_id=u-s4t2ud-c6b234d3edfab001ec93a17143651dcef4184d26390c68e82a5d64bd4ea6686e\
	&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fcallback%2F\
	&scope=public\
	&response_type=code\
	&state="

# identify from which page oauth2 was invoked
FROMLOGIN = 'd56b699830e77ba53855679cb1d252da'
FROMSIGNUP = '7d2abf2d0fa7c3a0c13236910f30bc43'

def signup_v(req):
    context = {
        'authorize_uri': authorize_uri+FROMSIGNUP,
        'show_alerts': True,
    }
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, f'Your account has been created! You are now able to log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    context['form'] = form
    return render(req, 'accounts/signup.html', context)

def login_v(req):
    context = {
        'authorize_uri': authorize_uri+FROMLOGIN,
        'show_alerts': True,
    }
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
    context['form'] = form
    return render(req, 'accounts/login.html', context)

"""
Callback for Oauth2 logic
--
catches tmp_code, exchanges it for an access token, use that
token to get user informations
"""
def callback(req):
    page_origin = req.GET.get('state')
    authorization_code = req.GET.get('code')
    if authorization_code is None:
        return HttpResponseBadRequest("Bad Request: Missing 'code' parameter")
    
    # exchange authorization code for access token
    o42 = Oauth42()
    token = o42.get_token(authorization_code)

    # use token to request user data
    user_data = o42.get_user_data(token)
    username_42 = user_data.get('login')
    email_42 = user_data.get('email')

    # when user is in database
    if username_42 in str(User.objects.all()):
        known_user = User.objects.get(username=username_42)
        if known_user.profile.isstudent:
            login(req, known_user)
            if 'next' in req.POST:
                return redirect(req.POST.get('next'))
            else:
                return redirect('home:welcome')
        else:
            if page_origin == FROMLOGIN:
                messages.warning(req, "The account you're trying to connect to was created without 42intra. Please enter your credentials to log in.")
                return redirect('accounts:login')
            else:
                messages.warning(req, f'The username <strong>{username_42}</strong> already exists. Pleaser enter another one.')
                return redirect('accounts:signup')
    # when user is NOT in database
    if page_origin == FROMLOGIN:
        messages.info(req, "No corresponding account was found. Please sign-up first.")
        return redirect('accounts:signup')
    elif page_origin == FROMSIGNUP:
        newUser = User.objects.create_user(username_42, email_42)
        newUser.profile.isstudent = True
        newUser.profile.save()
        messages.success(req, f'Your account has been created! You are now able to log in.')
        return redirect('accounts:login')

class Oauth42:
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
        messages.info(req, f'You have been logged out.')
        return redirect('home:welcome')

################################################################################

"""
Profile view of current user or another one
"""
@login_required(login_url='/accounts/login/')
def profile(request, username):
    context = {}
    try:
        displayed_user = User.objects.get(username=username)
    except:
        return render(request, '404.html', {
            'message': 'User not found',
            "show_alerts": True
        })
    if displayed_user:
        context['username'] = displayed_user.username
        context['email'] = displayed_user.email
        context['profile_img'] = displayed_user.profile.image.url
        context['wins'] = displayed_user.profile.wins
        context['losses'] = displayed_user.profile.losses

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != displayed_user:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        
        context["is_self"] = is_self
        context["is_friend"] = is_friend

    context['show_alerts'] = True

    return render(request, 'accounts/profile.html', context)

"""
Logic for deleting a user > profile > friendlist
"""
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

"""
Settings page for editing user info
"""
@login_required(login_url='/accounts/login/')
def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('accounts:profile_edit')
        messages.warning(request, 'NOT VALID')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/editprofile.html', context)