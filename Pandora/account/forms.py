from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import forms

from account.models import Author


class CustomUserCreateForm(forms.Form, UserCreationForm):
    class Meta:
        model = Author
        fields = ("username", 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}
