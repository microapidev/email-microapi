from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid.helpers.mail import *
from .serializers import EmailSchedulingSerializer
from django.template.loader import get_template
from rest_framework.parsers import MultiPartParser, FormParser
# from .tasks import send_mail
from rest_framework import mixins
from rest_framework import generics

from datetime import timedelta
from django.utils import timezone
from django_q.tasks import async_task, schedule
from django_q.models import Schedule

import os

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}

class SendSchduledEmail(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    @swagger_auto_schema(
        request_body=EmailSchedulingSerializer,
        operation_summary="Schedule an email",
        operation_description="",
        responses=MAIL_RESPONSES,
        tags=['Scheduled Email']
    )

    def post(self, request, *args, **kwargs):
        serializer= EmailSchedulingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            subject = serializer.validated_data['subject']
            body = serializer.validated_data['body']
            recipient = validated_data['recipient']
            sender = validated_data['sender']

            msg = 'You have schedduled an email'
        
            # # send this message right away
            async_task('django.core.mail.send_mail', 'You have scheduled an email', msg, sender, [recipient])
            
            # and this follow up email in one hour
            
            
            schedule('django.core.mail.send_mail', subject, body, sender, [recipient],
                schedule_type=Schedule.ONCE,
                next_run=timezone.now() + timedelta(seconds=10))
            
            return Response({
                'status': 'Successful',
                'data': {
                    'message': 'Scheduled email successfully sent'
                }
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
