from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account, UserSession

class UserRegistrationForm(UserCreationForm):
    ...

class UserUpdateForm(forms.ModelForm):
    ...

class ProfileUpdateForm(forms.ModelForm):
    ...