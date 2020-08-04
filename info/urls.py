from django.urls import path
from .views import *
from rest_framework import routers

'''
urlpatterns = [
	path('info/', InfoView.as_view(), name='info'),
]

'''
router = routers.DefaultRouter()
router.register(r'info', InfoViewSet)
urlpatterns = router.urls
