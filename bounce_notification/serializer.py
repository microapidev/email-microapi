from rest_framework import serializers


class BounceSerializer(serializers.Serializer):
    topic_arn = serializers.CharField(max_length=400)
    subscriber_email = serializers.EmailField()