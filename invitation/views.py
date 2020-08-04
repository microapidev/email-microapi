from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .serializers import InvitationMailSerializer
from django.template.loader import get_template, render_to_string
from sendgrid.helpers.mail import Content
from rest_framework import mixins
from rest_framework import generics
from .tasks import send_mail
from awsmail.tasks import send_aws_mail

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
        responses=MAIL_RESPONSES,
        tags=['Invitation Email']
    )

    def post(self, request, *args, **kwargs):
        if request.method=='POST':
            serializer = InvitationMailSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                

                site_name = validated_data.get('site_name')
                registration_page_link = validated_data.get('registration_link')
                recipient = validated_data.get('recipient')
                subject = 'User Invitation'
                description = validated_data.get('body')
                sender = validated_data.get('sender')
                html_content = render_to_string('invitation/email_invitation_template.html', {'sender': sender, 'site_name':site_name, 'description': description, 'registration_link':registration_page_link})
                content = Content("text/html", html_content)

                if validated_data.get('backend_type') == 'aws':
                    send_aws_mail(subject, '', sender, recipient, tmpl=html_content)
                    return Response({
                    'status': 'Successful',
                    'message': 'Invitation link successfully sent'
                }, status=status.HTTP_200_OK)
                    
                else:
                    send_mail(sender, recipient, subject, content)
                    return Response({
                    'status': 'Successful',
                    'message': 'Invitation link successfully sent'
                    }, status=status.HTTP_200_OK)
                    
            else:
                return Response({
                    'status': 'failure',
                    'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
                }, status=status.HTTP_400_BAD_REQUEST)


