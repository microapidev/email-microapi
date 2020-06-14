from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')