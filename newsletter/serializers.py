from rest_framework import serializers
from .models import Newsletter

class NewsletterSerializers(serializers.ModelSerializer):
    """Serializing fields/objects for creating and sending emails on the go"""
    class Meta:
        model = Newsletter
        fields = ('subject', 'body', 'from_email', 'to_email')


class CustomSerializers(serializers.ModelSerializer):
    """Serializing fields/objects for sending predefined newsletters"""
    class Meta:
        model = Newsletter
        fields = ('subject', 'from_email', 'to_email')