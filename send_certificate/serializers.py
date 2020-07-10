from rest_framework import serializers

class SendCertificatSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    participant_name = serializers.CharField()
    certificate_link = serializers.CharField()
    sender = serializers.EmailField()
