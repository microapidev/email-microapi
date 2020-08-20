from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
import pytest


settings =  [
    {
        'setting_name': 'SendGrid Credentials',
        'setting_type': 'list',
        'setting_key': 'SENDGRID_SMTP_CREDENTIALS',
        'setting_required': True,
        'setting_value':
        [
            {
                'setting_name': 'Sendgrid Api Key',
                'setting_value': None,
                'setting_required': True
            },
            {
                "setting_name": "Email Port",
                'setting_value': None,
                'setting_required': True
            },
            {
                'setting_name': 'TLS/SSL Setting',
                'setting_value': None,
                'setting_required': True
            },                
        ]
    },
    {
        'setting_name': 'Aws Settings Credentials',
        'setting_type': 'string',
        'setting_key': 'AWS_CREDENTIALS',
        'setting_required': True,
        'setting_value':
        [
            {
                'setting_name': 'AWS Access Key ID',
                'setting_value': None,
                'setting_required': True
            },
            {
                'setting_name': 'AWS Secret Access Key',
                'setting_value': None,
                'setting_required': True
            },
            {
                'setting_name': 'AWS Ses Region Name',
                'setting_value': None,
                'setting_required': True
            },
            {
                'setting_name': 'AWS Ses Region Endpoint',
                'setting_value': None,
                'setting_required': True
            }
        ]
    },   
    {
        'setting_name': 'Email Backend Type',
    },
]


class SettingsView(APIView):
    
    def get(self, request):
        data = {
            "message": "Settings retreived successfully!",
            "data": settings,
            "success": True           
        }
        return Response(data, status=status.HTTP_200_OK)

