from django.urls import path
from .views import awsMail

urlpatterns = [
    path('awsmail/', awsMail.as_view()),
]