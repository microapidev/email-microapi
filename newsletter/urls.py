from django.urls import path
from . import views

urlpatterns = [
    path('newsletter_all', views.DisplayAll.as_view(), name='DisplayAll'),
    path('create_newsletter/', views.CreateNewsletter.as_view(), name='CreateNewsletter'),
]