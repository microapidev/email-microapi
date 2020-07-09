from django.urls import path, include
from rest_framework import routers
from mail_app import views

# created a router and registered mail viewset with it.
router = routers.DefaultRouter()
router.register('send', views.MailViewset, base_name='send')

# the api urls are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
