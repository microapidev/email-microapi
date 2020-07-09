from django.urls import path
from . import views

urlpatterns = [
    path('send_certificate/', views.SendCertificateLink.as_view()),
]