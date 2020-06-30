from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .models import Newsletter
from django.conf import settings
from .serializers import NewsletterSerializer


MAIL_RESPONSES = {
    '200': 'Mail sent successfully.',
    '400': 'Incorrect request format.',
    '500': 'An error occurred, could not send email.' 
}
class DisplayAll(APIView):
    """Displays all the newsletters in the database"""
    @swagger_auto_schema(
		operation_description="Displays all the newsletters in the database.",
		responses=MAIL_RESPONSES
	)
    def get(self, request):
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializer(newsletters, many=True)
        return Response(serializer.data)


class CreateNewsletter(APIView):
    """Creates a newsletter"""
    @swagger_auto_schema(
		request_body=NewsletterSerializer,
		operation_description="Creates a newsletter.",
		responses=MAIL_RESPONSES
	)
    def post(self, request):
        newsletter = Newsletter.objects.create(subject=request.data['subject'],
                                                body=request.data['body'],
                                                email=request.data['email'],
                                                status=request.data['status'])
        serializer = NewsletterSerializer(newsletter)
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
        
