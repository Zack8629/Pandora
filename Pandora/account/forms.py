from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms

from account.models import Author


class CustomUserCreateForm(forms.Form, UserCreationForm):
    class Meta:
        model = Author
        fields = ("username", 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['username', 'first_name', 'last_name', 'email', 'about_me', 'birthday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
