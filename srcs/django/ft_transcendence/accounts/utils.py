from accounts.models import FriendRequest



def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.object.get(sender=sender, receiver=receiver, is_active=True)
    except FriendRequest.DoesNotExist:
        return False