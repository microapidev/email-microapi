from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'subject',
            'content',
            'recipient'
        ]


class EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'subject',
            'content',
            'recipient'
        ]

