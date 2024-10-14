from django.urls import path, include

urlpatterns = [
    # ...
    path('authentification/', include('authentification.urls')),
    # ...
]
