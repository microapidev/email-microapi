from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import MailSerializer, TemplateMailSerializer, UserSerializer, CustomTeplateMailSerializer
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

    @swagger_auto_schema(
        request_body=MailSerializer,
        operation_description="Sends email as plain text to recipient from sender.",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        mail_sz = MailSerializer(data=request.data)
        if mail_sz.is_valid():
            return send_email(mail_sz.validated_data)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
class SendMailWithTemplate(APIView):

    @swagger_auto_schema(
        request_body=TemplateMailSerializer,
        operation_description="Sends email as HTML template to recipient from sender.",
        responses=MAIL_RESPONSES
    )
    def post(self, request):
        template_mail_sz = TemplateMailSerializer(data=request.data)
        if template_mail_sz.is_valid():
            return send_email(template_mail_sz.validated_data, is_html_template=True)
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

class SendInvitationLink(APIView):

    @swagger_auto_schema(
        request_body=CustomTeplateMailSerializer,
        operation_description="Sends email invites",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        if request.method=='POST':
            sg = SendGridAPIClient()
            serializer = CustomTeplateMailSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                try:
                    email = request.user.email
                except AttributeError:
                    # if user has no email, which shouldnt happen, the org_email, takes the place of the sender
                    email = validated_data.get('org_email')
                site_name = validated_data.get('site_name')
                registration_page_link = validated_data.get('registration_link')
                to_email = validated_data.get('recipient')
                subject = 'User Invitation'
                description = validated_data.get('body')
                from_email = validated_data.get('org_email')
                html_content = get_template('email_invitation_template.html').render({'sender': email, 'site_name':site_name, 'description': description, 'registration_link':registration_page_link})
                content = Content("text/html", html_content)

                mail = Mail(from_email, to_email, subject, content)
                sg.send(mail)
                return Response({
                    'status': 'success',
                    'data': {'message': 'Invitation Sent Successfully'}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'failure',
                    'data': {'message': 'Something went wrong'}
                }, status=status.HTTP_501_NOT_IMPLEMENTED)

class SendConfirmationLink(APIView):
    @swagger_auto_schema(
        request_body=CustomTeplateMailSerializer,
        operation_description="Sends email confirmation links, it takes in parameters such as sender, recipient , body(which can be left empty), and tthe confirmation url",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        serializer= CustomTeplateMailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(validated_data['org_email'])
            context = {
                'sender': validated_data['org_email'],
                'domain_name': validated_data['site_name'],
                'description': validated_data['body'],
                'confirmation_link': validated_data['registration_link']
            }
            subject = 'Account Confirmation'
            mail_to = validated_data['recipient']
            mail_from = validated_data['org_email']
            html_content = get_template('confirmation_link_template.html').render(context)
            content = Content("text/html", html_content)

            mail = Mail(mail_from, mail_to, subject, content)
            sg.send(mail)
            return Response({
                'status': 'Successful',
                'message': 'Confirmation link successfully sent'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Failed',
                'message': 'Confirmation link could not be sent!'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendRegistrationMail(APIView):
    @swagger_auto_schema(
        request_body=CustomTeplateMailSerializer,
        operation_description="Sends email after user registers, it takes in parameters such as sender, recipient , body(which can be left empty), and tthe site url",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        serializer= CustomTeplateMailSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            context = {
                'sender': validated_data['org_email'],
                'domain_name': validated_data['site_name'],
                'description': validated_data['body'],
                'site_url': validated_data['registration_link']
            }
            subject = 'Welcome Esteemed Customer'
            mail_to = validated_data['recipient']
            mail_from = validated_data['org_email']
            html_content = get_template('welcome_mail_template.html').render(context)
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