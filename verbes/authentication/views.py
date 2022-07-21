from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.forms import LoginForm


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
