from rest_framework import serializers
from .models import GreetingsBC



class GreetingsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GreetingsBC
        fields = '__all__'