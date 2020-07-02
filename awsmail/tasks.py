from celery import task
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MailSerializer
from django.core.mail import send_mail
from time import sleep


@task
def send_aws(self, request):
    serializer = MailSerializer(data=request.data)
    if serializer.is_valid():
        subject = serializer.validated_data.get('subject')
        body = serializer.validated_data.get('body')
        sender = serializer.validated_data.get('sender')
        recipient = serializer.validated_data.get('recipient')
        
        response = send_mail(subject, body, sender, [recipient])

        return response
