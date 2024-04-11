from accounts.models import FriendRequest
import os
import requests

def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False

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
            return None
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
