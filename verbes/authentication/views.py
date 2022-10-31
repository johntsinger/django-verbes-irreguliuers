from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
    update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from authentication.forms import (LoginForm, SignupForm,
    MyPasswordChangeForm, EmailChangeForm, DeleteAccountForm)
from verbes_app.models import UserProfile, Verbe, Table, UserTable


def login_page(request):
    form = LoginForm()
    message = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('verbe-list')
        message = 'Identifiants invalides'
    return render(request,
        'authentication/login.html',
        {'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request,
        'authentication/signup.html',
        {'form': form})

@login_required
def parameters(request):
    if request.method == "POST":
        if 'change_password' in request.POST:
            password_form = MyPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) # Otherwise the user’s auth session will be invalidated and she/he will have to log in again.
                messages.success(request,
                    'Your password was successfully updated !')
                return redirect('parameters')
            else:
                messages.error(request, 'Please correct the errors below.')
        if 'change_email' in request.POST:
            email_form = EmailChangeForm(request.POST,
                initial={'current_email': request.user.email})
            if email_form.is_valid():
                user = request.user
                user.email = email_form.cleaned_data['new_email']
                user.save()
                messages.success(request,
                    'Your email was successfully updated !')
                return redirect('parameters')
            else:
                messages.error(request, 'Please correct the errors below.')
        if 'delete-account' in request.POST:
            delete_form = DeleteAccountForm(request.POST)
            if delete_form.is_valid():
                user = authenticate(
                    email=request.user.email,
                    password=delete_form.cleaned_data['password'],
                )
                if user is not None:
                    request.user.delete()
                    return redirect('/')
                else:
                    messages.error(request,
                        'The password you entered does not match your password.')
                    return redirect('parameters')
    else:
        password_form = MyPasswordChangeForm(request.user)
        email_form = EmailChangeForm(
            initial={'current_email': request.user.email})
        delete_form = DeleteAccountForm()
    return render(request,
        'authentication/parameters.html',
        {'password_form': password_form, 'email_form': email_form, 
        'email': request.user.email, 'delete_form': delete_form})
