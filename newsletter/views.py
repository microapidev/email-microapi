from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from .models import Newsletter
from django.core.mail import send_mail
from django.conf import settings
from .serializers import NewsletterSerializer


class DisplayAll(APIView):
    """Displays all the newsletters in the database"""
    def get(self, request):
        newsletters = Newsletter.objects.all()
        serializer = NewsletterSerializer(newsletters, many=True)
        return Response(serializer.data)


class CreateNewsletter(APIView):
    """Creates a newsletter in the database"""
    def post(self, request):
        newsletter = Newsletter.objects.create(subject=request.data['subject'],
                                                body=request.data['body'],
                                                is_html=request.data['is_html'],
                                                from_email=settings.EMAIL_HOST_USER,
                                                to_email=request.data['to_email'])
                                                #status=request.data['status'])
        serializer = NewsletterSerializer(data=newsletter)
        if serializer.is_valid():
            subject = serializer.validated_data.get('subject')
            body = serializer.validated_data.get('body')
            from_email = settings.EMAIL_HOST_USER
            to_email = serializer.validated_data.get('to_email')
            send_email = send_mail(subject, body, from_email, [to_email])
            send_email.send()
        else:
            return Response({'delivery_message': 'sent successfully'},
                            status=status.HTTP_201_CREATED)
        

def newsletter_view(request):
    return render(request, 'email_newletterx.html', {})


