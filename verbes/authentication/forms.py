from django import forms
from authentication.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput,
        )