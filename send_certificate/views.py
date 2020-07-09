from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import SendCertificatSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
from django.template.loader import get_template
from rest_framework import mixins
from rest_framework import generics
from django.core.mail import get_connection, send_mail

import os

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}

class SendCertificateLink(APIView):
    @swagger_auto_schema(
        request_body=SendCertificatSerializer,
        operation_summary="Predefined template to send out certificatee links to participants",
        operation_description="Sends certificate links, it takes in parameters such as sender, recipient , body(which can be left empty), and the link to download the certificate",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        serializer= SendCertificatSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['sender'],
                'team_name': validated_data['team_name'],
                'participant_name': validated_data.get('participant_name'),
                'certificate_link': validated_data['certificate_link']
            }
            subject = 'Certificate Of Achievement'
            mail_to = validated_data['recipient']
            mail_from = validated_data['sender']
            html_content = get_template('send_certificate/certificate_link.html').render(context)
            content = Content("text/html", html_content)

            # mail = Mail(mail_from, mail_to, subject, content)
            # sg.send(mail)
            with get_connection(
                backend='djcelery_email.backends.CeleryEmailBackend',
                host='smtp.sendgrid.net',
                port=587,
                username='apikey',
                password=os.getenv('SENDGRID_API_KEY'),
                use_tls=True
                ) as connection:
                send_mail(subject, '', mail_from, [mail_to], html_message=html_content, fail_silently=False, connection=connection)

            return Response({
                'status': 'Successful',
                'message': 'certificate link successfully sent'
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
