from rest_framework import serializers, fields
from rest_framework.validators import UniqueValidator

class EmailSchedulingSerializer(serializers.Serializer):
    sender = serializers.EmailField()
    recipient = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()
