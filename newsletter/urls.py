from django.urls import path
from . import views


urlpatterns = [
    path('newsletter_all/', views.DisplayAll.as_view()),
    path('create_newsletter/', views.SendEmail.as_view()),
    path('custom_newsletter/', views.SendCustomMail.as_view()),
]
