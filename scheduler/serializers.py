from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class EmailSchedulingSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    # body = serializers.CharField(required=False, allow_blank=True)
    sender = serializers.EmailField()
