from django.contrib import admin
from django.urls import path, include
from .views import login


urlpatterns = [
    # path('rest-auth/', include('rest_auth.urls')),
    path('login', login)
]