from django.shortcuts import render
from itertools import chain
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django_bouncy.models import Bounce, Complaint
from .serializers import BounceSerializer, ComplaintSerializer

class Notification(APIView):
	@swagger_auto_schema(
		operation_description="Processes bounces and complaints from AWS Simple Notification Service",
		operation_summary="Bounces and complaints notification",
	)

	def get(self, request):
		complaints = Complaint.objects.all()
		hard_bounces = Bounce.objects.filter(hard=True)

		# Create an iterator for the querysets and turn it into a list.
		query_list = list(chain(complaints, hard_bounces))

		# Build the list with items based on the ComplaintSerializer and BounceSerializer fields
		response = list()
		for entry in query_list:
			item_type = entry.__class__.__name__.lower()
			if isinstance(entry, Complaint):
				serializer = ComplaintSerializer(entry)
			if isinstance(entry, Bounce):
				serializer = BounceSerializer(entry)

			response.append({'item_type': item_type, 'data': serializer.data})

		return Response(response)

	