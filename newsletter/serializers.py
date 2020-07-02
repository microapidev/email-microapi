from rest_framework import serializers
from .models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('subject', 'body', 'email', 'status', 'created', 'updated')

