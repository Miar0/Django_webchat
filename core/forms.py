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


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    check_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = SocialUser
        fields = (
            'username',
            'email',
        )
        widgets = {
            'username': forms.widgets.TextInput(),
            'email': forms.widgets.EmailInput(),
        }
        help_texts = {
            'username': None
        }

    def clean_check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['check_password']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['check_password']

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user