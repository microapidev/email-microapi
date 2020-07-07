from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import RegistrationMailSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
from django.template.loader import get_template
from rest_framework import mixins
from rest_framework import generics


from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}


class SendRegistrationMail(APIView):
    @swagger_auto_schema(
        request_body=RegistrationMailSerializer,
        operation_summary="Predefined template for sending registration confirmation",
        operation_description="Sends email after user registers, it takes in parameters such as sender, recipient , body(which can be left empty), and tthe site url",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        serializer= RegistrationMailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['sender'],
                'domain_name': validated_data['site_name'],
                'description': validated_data['body'],
                'site_url': validated_data['registration_link']
            }
            subject = 'Welcome Esteemed Customer'
            mail_to = validated_data['recipient']
            mail_from = validated_data['sender'] 
            html_content = get_template('registration/welcome_mail_template.html').render(context)
            content = Content("text/html", html_content)

            mail = Mail(mail_from, mail_to, subject, content)
            sg.send(mail)
            return Response({
                'status': 'Successful',
                'message': 'Welcome mail successfully sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Failed',
                'message': 'Welcome mail could not be sent!'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
