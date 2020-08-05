from django.shortcuts import render
from send_email_microservice.views import SettingsView
# Create your views here.

def test_settings_view():
    data = {
        "message": "Settings retreived successfuly",
        "data": settings,
        "success": True
    }
    assert Response.status_code == status.HTTP_200_OK
    assert data['data'] == settings
    return Response("worked!")