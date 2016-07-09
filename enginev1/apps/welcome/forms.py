from django import forms
from django.contrib.auth.models import User
from .models import Client


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'display_name', 'alpha_label', 'beta_label')