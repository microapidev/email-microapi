from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('sendmail', views.SendMail.as_view()),
    path('sendmailwithtemplate', views.SendMailWithTemplate.as_view()),
    path('register', views.UserCreate.as_view(), name='account-create'),
    path('send_invitation_link/', csrf_exempt(views.send_invitation_link)),
]