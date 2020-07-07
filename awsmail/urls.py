from django.urls import path
from .views import AwsMail

urlpatterns = [
    path('awsmail/', AwsMail.as_view()),
]