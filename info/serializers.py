from rest_framework import serializers
from .models import Info

class InfoSerializer(serializers.ModelSerializer):
	icon = serializers.ImageField(use_url=True, max_length=None)
	class Meta:
		model = Info
		fields = ('title', 'description', 'icon',)