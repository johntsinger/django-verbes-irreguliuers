from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from authentication.forms import LoginForm, SignupForm
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