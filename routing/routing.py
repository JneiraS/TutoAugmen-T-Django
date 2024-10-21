from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Vous pouvez ajouter d'autres motifs d'URL ici si nécessaire
]
