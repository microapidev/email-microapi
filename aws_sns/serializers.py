from rest_framework import serializers
from django_bouncy.models import Bounce, Complaint

class BounceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bounce
		fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
	class Meta:
		model = Complaint
		fields = '__all__'

