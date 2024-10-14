from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
    return render(request, 'authentification/login.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect(reverse('polls:index'))
