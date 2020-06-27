from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from .serializers import MailSerializer, TemplateMailSerializer, UserSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.views.generic import UpdateView
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string

from datetime import datetime, timedelta
import time


"""def sample_template(subject_filename, text_body_filename, html_template, **plaintext_context, **context):
    plaintext_context = Context(autoescape=False) # HTML escaping not appropriate in plaintext
    subject_file = render_to_string(subject_filename, plaintext_context)
    text_body_file = render_to_string(text_body_filename, plaintext_context)
    html_template_file = render_to_string(html_template, context=context)

    templates = [subject_file, text_body_file, html_template_file]

    return templates

    # msg = EmailMultiAlternatives(subject=subject, from_email=from_email,
                                    # to=[to], body=text_body)
    # msg.attach_alternative(html_body, "text/html")
    # msg.send()"""



MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}

class UserCreate(APIView):
    """ 
    Creates the user. 
    """
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_description="Create an account to generate a token",
    )
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)

            resp = { 'status': 'success', 'data': { 'message': 'Account created successfully.' } }
            resp['data']['account_id'] = user.username
            resp['data']['access_token'] = token.key

            return Response(resp, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMail(APIView):

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=MailSerializer,
        operation_description="Sends email as plain text to recipient from sender.",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        mail_sz = MailSerializer(data=request.data)
        if mail_sz.is_valid():
            return send_email(request, mail_sz.validated_data)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)

class SendMailWithTemplate(APIView):

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=TemplateMailSerializer,
        operation_description="Sends email as HTML template to recipient from sender.",
        responses=MAIL_RESPONSES
    )

    def post(self, request):
        template_mail_sz = TemplateMailSerializer(data=request.data)
        if template_mail_sz.is_valid():
            return send_email(request, template_mail_sz.validated_data, is_html_template=True)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': template_mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
            

class SendScheduledMail(APIView):

    #permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=MailSerializer,
        operation_description="Sends email pre-scheduled mail as plaintext.",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        mail_sz = MailSerializer(data=request.data)
        if mail_sz.is_valid():
            send_email(request, mail_sz.validated_data, False, scheduled=True)

        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)


def send_email(request, options, is_html_template=False, scheduled=False):

    def get_email_dict(emails, delimeter):
        return [{'email': email.strip()} for email in emails.split(delimeter)]

    body_type = 'text/plain'
    body = ''

    if is_html_template:
        body_type = 'text/html'
        body = options['htmlBody']
              
    else:
        body = options['body']

    # To send the mail at a scheduled date
    if(scheduled):
        # Get present date/time
        current_time = datetime.now() # Get timestamp of current time
        time_to_send = options['time_to_send'] # Get the datetime object from the serializer option

        future_in_epoch = datetime.timestamp(time_to_send) # Convert datetime object to POSIX timestamp in place
        secs = future_in_epoch - datetime.timestamp(current_time) # Timedelta between current time and scheduled time in epoch seconds      
        
        # Convert the time to timestamp
        # later_timestamp = datetime.timestamp(later_time) 
        data = {
        'personalizations': [{
            'to': [{'email': options['recipient']}],
            'subject': options['subject'],
            'send_at': future_in_epoch
        }],
        'from': {'email': request.user.email},
        'content': [{
            'type': body_type,
            'value': body
        }],
    }
    else:
        data = {
        'personalizations': [{
            'to': [{'email': options['recipient']}],
            'subject': options['subject']
        }],
        'from': {'email': request.user.email},
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
    try: 
        sg.client.mail.send.post(request_body=data)

    except:
        return Response({
            'status': 'failure',
            'data': { 'message': 'An error occurred, could not send email.'}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'success',
        'data': { 'message': 'Mail sent successfully.'}
    }, status=status.HTTP_200_OK)