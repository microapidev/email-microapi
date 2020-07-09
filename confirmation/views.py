from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import ConfirmationMailSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
from django.template.loader import get_template
from rest_framework import mixins
from rest_framework import generics
from django.core.mail import get_connection, send_mail


from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

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
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        serializer= ConfirmationMailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['sender'],
                'domain_name': validated_data['site_name'],
                'description': validated_data.get('body'),
                'confirmation_link': validated_data['registration_link']
            }
            print(validated_data.get('body'))
            subject = 'Account Confirmation'
            mail_to = validated_data['recipient']
            mail_from = validated_data['sender']
            html_content = get_template('confirmation/confirmation_link_template.html').render(context)
            content = Content("text/html", html_content)

            # mail = Mail(mail_from, mail_to, subject, content)
            # sg.send(mail)
            connector = get_connection(
                backend='djcelery_email.backends.CeleryEmailBackend',
                host='smtp.sendgrid.net',
                port=587,
                username='apikey',
                password='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',
                use_tls=True
            )
            send_mail(subject, '', mail_from, [mail_to], html_message=html_content, fail_silently=False, connection=connector)

            return Response({
                'status': 'Successful',
                'message': 'Confirmation link successfully sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
