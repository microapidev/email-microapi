from django.urls import path
from . import views

urlpatterns = [
	path('settings_config/', views.SettingsConfig.as_view(), name='settings-config'),
	path('settings_config/<str:sender>/', views.SettingsConfigDetail.as_view(), name='settings-config-detail')
]