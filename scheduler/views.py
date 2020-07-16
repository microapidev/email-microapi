from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid.helpers.mail import *
from .serializers import EmailSchedulingSerializer
from django.template.loader import get_template
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
    @swagger_auto_schema(
        request_body=EmailSchedulingSerializer,
        operation_summary="Predefined template to send confirmation email",
        operation_description="Sends email confirmation links, it takes in parameters such as sender, recipient , body(which can be left empty), and the confirmation url",
        responses=MAIL_RESPONSES,
        tags=['Scheduled Email']
    )

    def post(self, request, *args, **kwargs):
        serializer= EmailSchedulingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            subject = 'Scheduled Email'
            body = 'This is a scheduled email, you will receive a follow up email in 10 seconds'
            recipient = validated_data['recipient']
            sender = validated_data['sender']
        
            # # send this message right away
            async_task('django.core.mail.send_mail', subject, body, sender, [recipient])
            
            # and this follow up email in one hour
            msg = 'Here are some tips to get you started...'
            
            schedule('django.core.mail.send_mail', 'Follow up', msg, sender, [recipient],
                schedule_type=Schedule.ONCE,
                next_run=timezone.now() + timedelta(seconds=10))
            
            return Response({
                'status': 'Successful',
                'data': {
                    'message': 'Confirmation link successfully sent'
                }
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
