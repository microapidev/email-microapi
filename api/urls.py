from django.urls import path
from . import views, include

urlpatterns = [
    path('sendmail', views.SendMail.as_view()),
    path('sendmailwithtemplate', views.SendMailWithTemplate.as_view()),
    path('register', views.UserCreate.as_view(), name='account-create'),
    path('accounts/', include('django.contrib.auth.urls')),
]