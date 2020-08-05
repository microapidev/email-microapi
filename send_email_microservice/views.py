from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.views import APIView
import pytest


settings =  [
    {
        'setting_name':'SendGrid Credentials',
        'setting_type':'list',
        'setting_key':'SENDGRID_SMTP_CREDENTIALS',
        'setting_required':True,
        'setting_value':
        [
            {
                'setting_name':'Sendgrid Api Key',
                'setting_type':'string',
                'setting_key':'SENDGRID_API_KEY',
                'setting_value':None,
                'setting_required':True,
            },
            {
                "setting_name":"Email Port",
                'setting_type':'integer',
                'setting_key':'EMAIL_PORT',
                'setting_value':None,
                'setting_required':True
            },
            {
                'setting_name':'TLS/SSL Setting',
                'setting_type':'boolean',
                'setting_key':'EMAIL_USE_TLS',
                'setting_value':None,
                'setting_required':True
            },                
        ]
    },

    {
        'setting_name':'Aws Settings Credentials',
        'setting_type':'string',
        'setting_key':'AWS_CREDENTIALS',
        'setting_required':True,
        'setting_value':
        [
            {
                'setting_name':'AWS Access Key ID',
                'setting_type':'string',
                'setting_key':'AWS_ACCESS_KEY_ID',
                'setting_value':None,
                'setting_required':True
            },
            {
                'setting_name':'AWS Secret Access Key',
                'setting_type':'string',
                'setting_key':'AWS_SECRET_ACCESS_KEY',
                'setting_value':'string',
                'setting_required':True
            },
            {
                'setting_name':'AWS Ses Region Name',
                'setting_type':'string',
                'setting_key':'AWS_SES_REGION_NAME',
                'setting_value':None,
                'setting_required':True
            },
            {
                'setting_name':'AWS Ses Region Endpoint',
                'setting_type':'string',
                'setting_key':'AWS_SES_REGION_ENDPOINT',
                'setting_value':None,
                'setting_required':True
            }
        ]
    },

    {
        'setting_name':'Email Backend Type',
        'setting_type':'string',
        'setting_key':'backend_type',
        'setting_value':None,
        'setting_required':True
    },
]


class ReturnSettings(APIView):
    def get(self, request):
        data = {
            "message":"Settings retreived successfuly",
            "data":settings,
            "success":True
        }
        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)



class test_settings(APIView):
    def get(self, request):
        data = {
            "message":"Settings retreived successfuly",
            "data":settings,
            "success":True
        }
        assert Response.status_code == status.HTTP_200_OK
        assert data['data'] == settings
        return Response("worked!")
