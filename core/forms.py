from django import forms
from core.models import *


class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequests
        fields = ['to_user']


class AcceptFriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequests
        fields = ['accepted']
