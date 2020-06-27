from django.urls import path
from .views import awsEmail

urlpatterns = [
    path('awsEmail', awsEmail.as_view()),
]