from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User


class RegistrationMailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    body = serializers.CharField(required=False, allow_blank=True)
    site_name = serializers.CharField()
    registration_link = serializers.CharField()
    sender = serializers.EmailField()
    backend_type = serializers.CharField(required=False, allow_blank=True)