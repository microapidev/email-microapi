from django.urls import path
from . import views


urlpatterns = [
    path('bounce_notifications/', views.BounceNotification.as_view() name='BounceNotification'),
]