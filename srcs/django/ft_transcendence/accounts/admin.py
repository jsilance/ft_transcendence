from django.contrib import admin
from .models import Profile, FriendList, FriendRequest

# Register your models here.
admin.site.register(Profile)

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FriendList

admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender', 'receiver']
    search_fields = ['sender__username', 'sender_email', 'receiver_email', 'receiver_username']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)
