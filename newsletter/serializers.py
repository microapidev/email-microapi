from rest_framework import serializers
from .models import Newsletter

class NewsletterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('subject', 'body', 'from_email', 'to_email')


class CustomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('subject', 'from_email', 'to_email')