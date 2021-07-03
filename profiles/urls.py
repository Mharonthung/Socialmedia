from django.urls import path
from .views import (
    my_profile_view, 
    invites_received_view, 
    ProfileListView, 
    ProfileDetailView,
    invite_profiles_list_view,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation,
    friends,
)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name="all_profile_view"),
    path('myprofile/', my_profile_view, name="my_profile_view"),
    path('my-invites/', invites_received_view, name="my_invites_view"),
    path('to-invite/', invite_profiles_list_view, name="invite_profile_view"),
    path('send-invite/', send_invitation, name="send_invite"),
    path('remove-friend/', remove_from_friends, name="remove-friend"),
    path('<slug>', ProfileDetailView.as_view(), name="profile_detail_view"),  
    path('accept/', accept_invitation, name="accept_invitation"),
    path('reject/', reject_invitation, name="reject_invitation"), 
    path('friends/', friends, name="friends_list"),
]