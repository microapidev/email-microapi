from django.urls import path
from . import views

urlpatterns = [
    path('sendmail/', views.SendMail.as_view()),
    path('sendmailwithtemplate/', views.SendMailWithTemplate.as_view())
]