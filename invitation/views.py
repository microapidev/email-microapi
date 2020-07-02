from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from .serializers import InvitationMailSerializer
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
class SendInvitationLink(APIView):

    @swagger_auto_schema(
        request_body=InvitationMailSerializer,
        operation_summary="Predefined template for sending invitation link",
        operation_description="Sends email invites",
        responses=MAIL_RESPONSES
    )

    def post(self, request, *args, **kwargs):
        if request.method=='POST':
            sg = SendGridAPIClient()
            serializer = InvitationMailSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                try:
                    email = request.user.email
                except AttributeError:
                    # if user has no email, which shouldnt happen, the org_email, takes the place of the sender
                    email = validated_data.get('sender')
                site_name = validated_data.get('site_name')
                registration_page_link = validated_data.get('registration_link')
                to_email = validated_data.get('recipient')
                subject = 'User Invitation'
                description = validated_data.get('body')
                from_email = validated_data.get('sender')
                html_content = get_template('invitation/email_invitation_template.html').render({'sender': email, 'site_name':site_name, 'description': description, 'registration_link':registration_page_link})
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


