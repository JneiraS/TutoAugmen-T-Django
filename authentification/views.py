from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous êtes maintenant connecté.")
            return redirect(reverse('polls:index'))
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'authentification/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect(reverse('polls:index'))
