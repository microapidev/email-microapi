from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from .serializers import MailSerializer, TemplateMailSerializer, UserSerializer
from send_email_microservice.settings import SENDGRID_API_KEY
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
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

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
            return send_email(mail_sz.validated_data)
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
            return send_email(template_mail_sz.validated_data, is_html_template=True)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': template_mail_sz.errors}
            }, status=status.HTTP_400_BAD_REQUEST)

def send_email(options, is_html_template=False):

    def get_email_dict(emails, delimeter):
        return [{'email': email.strip()} for email in emails.split(delimeter)]

    body_type = 'text/plain'
    body = ''

    if is_html_template:
        body_type = 'text/html'
        body = options['htmlBody']
    else:
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
    try: sg.client.mail.send.post(request_body=data)
    except:
        return Response({
            'status': 'failure',
            'data': { 'message': 'An error occurred, could not send email.'}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'success',
        'data': { 'message': 'Mail sent successfully.'}
    }, status=status.HTTP_200_OK)
