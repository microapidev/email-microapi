from django.urls import path
from . import views

urlpatterns = [
	path('settings/', views.SettingsView.as_view(), name='settings'),
	path('settings_config/', views.SettingsConfig.as_view(), name='settings-config'),
	path('settings_config/<str:sender>/', views.SettingsConfigDetail.as_view(), name='settings-config-detail')
]