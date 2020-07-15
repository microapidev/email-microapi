from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
#from send_email_microservice.settings import UPLOADED_FILES_USE_URL

class MailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    sender = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()
    cc = serializers.CharField(required=False, allow_blank=True)
    bcc = serializers.CharField(required=False, allow_blank=True)

class TemplateMailSerializer(MailSerializer):
    body = None
    htmlBody = serializers.CharField()

class MailAttachmentSerializer(MailSerializer):
	attach = serializers.FileField(max_length=None, allow_empty_file=False, use_url=False)
