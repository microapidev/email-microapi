from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid.helpers.mail import *
from .serializers import ConfirmationMailSerializer
from django.template.loader import get_template
from .tasks import send_mail
from rest_framework import mixins
from rest_framework import generics
from awsmail.tasks import send_aws_mail

import os

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}

class SendConfirmationLink(APIView):
    @swagger_auto_schema(
        request_body=ConfirmationMailSerializer,
        operation_summary="Predefined template to send confirmation email",
        operation_description="Sends email confirmation links, it takes in parameters such as sender, recipient , body(which can be left empty), and the confirmation url",
        responses=MAIL_RESPONSES,
        tags=['Confirmation Email']
    )

    def post(self, request, *args, **kwargs):
        serializer= ConfirmationMailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['sender'],
                'domain_name': validated_data['site_name'],
                'description': validated_data.get('body'),
                'confirmation_link': validated_data['registration_link']
            }
            print(validated_data.get('backend_type'))
            subject = 'Account Confirmation'
            recipient = validated_data['recipient']
            sender = validated_data['sender']
            html_content = get_template('confirmation/confirmation_link_template.html').render(context)
            content = Content("text/html", html_content)

            if validated_data.get('backend_type') == 'aws':
                send_aws_mail(subject, content, sender, recipient)
                return Response({
                'status': 'Successful',
                'message': 'Confirmation link successfully sent'
            }, status=status.HTTP_200_OK)
                
            else:
                send_mail(sender, recipient, subject, content)
                return Response({
                'status': 'Successful',
                'message': 'Confirmation link successfully sent'
            }, status=status.HTTP_200_OK)
            
            
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
