from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput,
        )


class SignupForm(UserCreationForm):
    class Media:
        css = {
            'all': ('verbes_app/css/custom_forms.css',)
        }

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
        widgets = {
            'username': forms.fields.TextInput(
                attrs={'placeholder': User._meta.get_field('username').verbose_name})
        }