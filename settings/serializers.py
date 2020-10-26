from rest_framework import serializers
from .models import Settings

class SettingsSerializer(serializers.ModelSerializer):
	sg_api_key = serializers.CharField(allow_blank=True, required=False)
	access_key_id = serializers.CharField(allow_blank=True, required=False)
	secret_access_key = serializers.CharField(allow_blank=True, required=False)
	region_name = serializers.CharField(allow_blank=True, required=False)
	region_endpoint = serializers.CharField(allow_blank=True, required=False)

	class Meta:
		model = Settings
		fields = ('sender', 'backend_type', 'sg_api_key', 'access_key_id',
		     'secret_access_key', 'region_name', 'region_endpoint',)



	