from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid.helpers.mail import *
from .serializers import SendCertificateSerializer
from django.template.loader import get_template
from .tasks import send_mail
from rest_framework import mixins
from rest_framework import generics
from awsmail.tasks import send_aws_mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import os

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}

class SendCertificateLink(APIView):
    @swagger_auto_schema(
        request_body=SendCertificateSerializer,
        operation_summary="Predefined template to send out certificatee links to participants",
        operation_description="Sends certificate links, it takes in parameters such as sender, recipient , and the link to download the certificate, you can also specify what type of service to send mail with amazon or SMTP.",
        responses=MAIL_RESPONSES,
        tags=['Certificate Email']
    )

    def post(self, request, *args, **kwargs):
        serializer= SendCertificateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['sender'],
                'participant_name': validated_data.get('participant_name'),
                'certificate_link': validated_data['certificate_link']
            }
            subject = 'Certificate Of Achievement'
            recipient = validated_data['recipient']
            sender = validated_data['sender']
            html_content = get_template('send_certificate/certificate_link.html').render(context)
            content = Content("text/html", html_content)

            if validated_data.get('backend_type') == 'aws':
                send_aws_mail(subject, '', sender, recipient, tmpl=html_content)
                return Response({
                    'message': 'Certificate link successfully sent',
                    'success': True
            }, status=status.HTTP_200_OK)
                
            else:
                send_mail(sender, recipient, subject, content)
                return Response({
                    'message': 'Certificate link successfully sent',
                    'success': True
            }, status=status.HTTP_200_OK)
            
            
        else:
            return Response({
                'message': 'Incorrect request format.',
                'errors': serializer.errors,
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
