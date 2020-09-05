from rest_framework.response import Response
from rest_framework import status, generics
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework import generics
from .models import Settings
from .serializers import SettingsSerializer
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

class SettingsConfig(APIView):
	
	def post(self, request, *args, **kwargs):
		serializer = SettingsSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			if serializer.validated_data['backend_type'] == 'aws':
				serializer.save()
				return Response({
					'message': 'AWS config retrieved successfully!',
					'data': {
						'sender': serializer.data['sender'],
						'backend_type': serializer.data['backend_type'],
						'access_key_id': serializer.data['access_key_id'],
						'secret_access_key': serializer.data['secret_access_key'],
						'region_name': serializer.data['region_name'],
						'region_endpoint': serializer.data['region_endpoint']
					},
					'success': True}, status=status.HTTP_201_CREATED)
			else:
				serializer.save()
				return Response({
					'message': 'SMTP config retrieved successfully!',
					'data': {
						'sender': serializer.data['sender'],
						'backend_type': serializer.data['backend_type'],
						'sg_api_key': serializer.data['sg_api_key']
					},
					'success': True
					}, status=status.HTTP_201_CREATED)
		return Response({
			'message': 'bad request!',
			'errors': serializer.errors,
			'success': False}, status=status.HTTP_400_BAD_REQUEST)

class SettingsConfigDetail(APIView):

	def get_object(self, sender):
		try:
			return Settings.objects.get(sender=sender)
		except Settings.DoesNotExist:
			raise Http404

	def get(self, request, sender, format=None, *args, **kwargs):
		setting = self.get_object(sender)
		serializer = SettingsSerializer(setting)
		if serializer.data['backend_type'] == 'aws':
			return Response({
				'message': 'AWS config detail retrieved successfully!',
				'data': {
					'sender': serializer.data['sender'],
					'backend_type': serializer.data['backend_type'],
					'access_key_id': serializer.data['access_key_id'],
					'secret_access_key': serializer.data['secret_access_key'],
					'region_name': serializer.data['region_name'],
					'region_endpoint': serializer.data['region_endpoint']
				},
				'success': True}, status=status.HTTP_200_OK)
		else:
			return Response({
				'message': 'SMTP config detail retrieved successfully!',
				'data': {
					'sender': serializer.data['sender'],
					'backend_type': serializer.data['backend_type'],
					'sg_api_key': serializer.data['sg_api_key']
				},
				'success': True
				}, status=status.HTTP_200_OK)

	def put(self, request, sender, format=None, *args, **kwargs):
		setting = self.get_object(sender)
		serializer = SettingsSerializer(setting, data=request.data)
		if serializer.is_valid(raise_exception=True):
			if serializer.validated_data['backend_type'] == 'aws':
				serializer.save()
				return Response({
					'message': 'AWS config updated successfully!',
					'data': {
						'sender': serializer.data['sender'],
						'backend_type': serializer.data['backend_type'],
						'access_key_id': serializer.data['access_key_id'],
						'secret_access_key': serializer.data['secret_access_key'],
						'region_name': serializer.data['region_name'],
						'region_endpoint': serializer.data['region_endpoint']
					},
					'success': True}, status=status.HTTP_201_CREATED)
			else:
				serializer.save()
				return Response({
					'message': 'SMTP config updated successfully!',
					'data': {
						'sender': serializer.data['sender'],
						'backend_type': serializer.data['backend_type'],
						'sg_api_key': serializer.data['sg_api_key']
					},
					'success': True
					}, status=status.HTTP_201_CREATED)
		return Response({
			'message': 'bad request!',
			'errors': serializer.errors,
			'success': False
			}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, sender, format=None):
		setting = self.get_object(pk)
		setting.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

