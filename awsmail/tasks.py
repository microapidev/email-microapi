from celery import shared_task
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MailSerializer
from django.core.mail import send_mail
from time import sleep


@shared_task
def send_aws(self, request):
    serializer = MailSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        subject = serializer.validated_data.get('subject')
        body = serializer.validated_data.get('body')
        sender = serializer.validated_data.get('sender')
        recipient = serializer.validated_data.get('recipient')
        response = send_mail(subject, body, sender, [recipient])

        return Response({
                    'status': 'success',
                    'data': {'message': 'Mail Sent Successfully'}
                }, status=status.HTTP_200_OK)
