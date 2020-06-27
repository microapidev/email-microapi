from django.urls import path
from .views import awsEmail

urlpatterns = [
    path('awsemail/', awsEmail.as_view()),
]