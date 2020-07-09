
from rest_framework import serializers

class MailSerializer(serializers.Serializer):
   email_id = serializers.CharField()
   email_content = serializers.CharField()