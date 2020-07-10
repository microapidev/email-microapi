from django.urls import path
from . import views


urlpatterns = [
    path('newsletter_all/', views.DisplayAll.as_view(), name='DisplayAll'),
    path('create_newsletter/', views.SendEmail.as_view(), name='SendEmail'),
    path('custom_newsletter/', views.SendCustomMail.as_view(), 'SendCustomMail'),
]
