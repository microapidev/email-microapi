from mail_app import tasks
from .serializers import MailSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class MailViewset(viewsets.ViewSet):
    '''
    Email endpoint which receives email address and email HTML content
    '''

    def create(self, request):
        try:
            ip_data = request.data
            subject, sender = 'drf_celery_email_api_test', 'smtp.sendgrid.net' #a valid mail is required here
            serialized = MailSerializer(request.data).data
            receiver = serialized['email_id']
            if '@' not in receiver:
                raise Exception
            # html_content = '<h1>hey!! It worked</h1>'
            html_content = serialized['email_content']
            result = tasks.send_mail(subject, sender, receiver, html_content)
            if result == 'success':
                return Response('Mail sent successfully')
            else:
                raise Exception
        except:
            return Response('Error in sending mail')
