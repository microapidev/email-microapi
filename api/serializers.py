from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import GreetingsBC

class MailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    sender = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()
    cc = serializers.CharField(required=False, allow_blank=True)
    bcc = serializers.CharField(required=False, allow_blank=True)

class CustomTemplateMailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    body = serializers.CharField(required=False, allow_blank=True)
    site_name = serializers.CharField()
    registration_link = serializers.CharField()
    sender = serializers.EmailField()

class TemplateMailSerializer(MailSerializer):
    body = None
    htmlBody = serializers.CharField()

class GreetingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GreetingsBC
        fields = '__all__'