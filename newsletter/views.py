from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Newsletter
from .tasks import send_email, send_custom_mail
from .serializers import NewsletterSerializers, CustomSerializers


MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}


class DisplayAll(APIView):
    """Displays all the newsletters in the database"""
    def get(self, request):
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializers(newsletters, many=True)
        return Response(serializer.data)



class SendNewsletter(APIView):
    """Creates a newsletter"""
    @swagger_auto_schema(
		request_body=NewsletterSerializer,
		operation_description="Sends a newsletter.",
		responses=MAIL_RESPONSES
	)

    def post(self, request):
        #creating the objects to be saved to the database
        newsletter = Newsletter.objects.create(subject=request.data['subject'],
                                                            body=request.data['body'],
                                                            from_email=settings.EMAIL_HOST_USER,
                                                            to_email=request.data['to_email'])
        serializer = NewsletterSerializers(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data.get('subject')
            body = serializer.validated_data.get('body')
            from_email = settings.EMAIL_HOST_USER
            to_email = serializer.validated_data.get('to_email')
            #Using a celery task to send the email created above
            message = send_email.delay(subject, body, from_email, [to_email])
            return Response({'status': 'success',
                            'data': {'message': 'Mail Sent Successfully'}},
                            status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)


class SendCustomMail(APIView):
    """Sends custom(Predefined) Newsletters"""
    @swagger_auto_schema(
		request_body=NewsletterSerializers,
		operation_description="Sends predefined templates.",
		responses=MAIL_RESPONSES
	)
    def post(self, request):
        serializer = CustomSerializers(data=request.data)
        if serializer.is_valid():
            #validating objects before sending them as emails
            subject = serializer.validated_data.get('subject')
            from_email = settings.EMAIL_HOST_USER
            to_email = serializer.validated_data.get('to_email')
            with open(settings.BASE_DIR + '/newsletters/templates/newsletter.txt') as f:
                newsletter_mail = f.read()
            message = EmailMultiAlternatives(subject, newsletter_mail, from_email, [to_email])
            html_template = get_template('newsletter_1.html').render()
            message.attach_alternative(html_template, 'text/html')
            #using a celery task to send the html_templated email
            send_custom_mail.send.delay()
            return Response({'status': 'success',
                        'data': {'message': 'Mail Sent Successfully'}},
                        status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'failure',
                'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
            }, status=status.HTTP_400_BAD_REQUEST)
