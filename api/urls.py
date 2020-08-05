from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('sendmail/', views.SendMail.as_view(), name = "sendmail"),
    path('sendmailwithtemplate/', views.SendMailWithTemplate.as_view()),
]