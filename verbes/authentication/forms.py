from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # Adding class to signup form input
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'signup-input'


class MyPasswordChangeForm(PasswordChangeForm):
    change_password = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class EmailChangeForm(forms.Form):
    change_email = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    current_email = forms.EmailField(disabled=True)
    new_email = forms.EmailField()


class DeleteAccountForm(forms.Form):
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
    template_name = "authentication/delete_account_form.html"
