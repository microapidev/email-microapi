from django.urls import path
from .views import *

urlpatterns = [
	path('info/', InfoView.as_view(), name='info'),
]
