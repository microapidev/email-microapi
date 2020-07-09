from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import MailSerializer, TemplateMailSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
from django.template.loader import get_template
from rest_framework import mixins
from rest_framework import generics
from api.tasks import send_grid


from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}
BC_RESPONSES = {
    '200': 'GET request successful',
    '500': 'An error occurred, request could not be completed.'
}

class SendMail(APIView):

    @swagger_auto_schema(
        request_body=MailSerializer,
        operation_description="Sends email as plain text to recipient from sender.",
        operation_summary="Send plain email using SMTP (sendgrid)",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        mail_sz = MailSerializer(data=request.data)
        if mail_sz.is_valid():
            return send_grid.delay(mail_sz.validated_data)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
class SendMailWithTemplate(APIView):

    @swagger_auto_schema(
        request_body=TemplateMailSerializer,
        operation_description="Sends email as HTML template to recipient from sender.",
        operation_summary="Send email with html body using SMTP (sendgrid)",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        template_mail_sz = TemplateMailSerializer(data=request.data)
        if template_mail_sz.is_valid():
            return send_grid(template_mail_sz.validated_data, is_html_template=True)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': template_mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)


def send_email(options, is_html_template=False):
    def get_email_dict(emails, delimeter):
        return [{'email': email.strip()} for email in emails.split(delimeter)]
    if is_html_template:
        body_type = 'text/html'
        body = options['htmlBody']
    else:
        body_type = 'text/plain'
        body = options['body']
    data = {
        'personalizations': [{
            'to': [{'email': options['recipient']}],
            'subject': options['subject']
        }],
        'from': {'email': options['sender']},
        'content': [{
            'type': body_type,
            'value': body
        }],
    }
    if len(options['cc']) > 0:
        data['personalizations'][0]['cc'] = get_email_dict(options['cc'], ',')
    if len(options['bcc']) > 0:
        data['personalizations'][0]['bcc'] = get_email_dict(options['bcc'], ',')
    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.client.mail.send.post(request_body=data)
    if response.status_code != 202:
        return Response({
            'status': 'failure',
            'data': { 'message': 'An error occurred.'}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'success',
        'data': { 'message': 'Mail sent successfully.'}
    }, status=status.HTTP_200_OK)