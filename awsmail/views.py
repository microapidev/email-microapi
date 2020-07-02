from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import MailSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from rest_framework import status
from .tasks import send_aws

MAIL_RESPONSES = {
	'200': 'Mail sent successfully.',
	'400': 'Incorrect request format.',
	'500': 'An error occurred, could not send email.' 
}

"""
Send email using AWS Simple Email Service (SES)
"""

class AwsMail(APIView):
	@swagger_auto_schema(
		request_body=MailSerializer,
		operation_description="Send email using Simple Email Service from AWS",
		operation_summary="Sending email with Simple Email Service",
		responses=MAIL_RESPONSES
	)

	def post(self, request):
		mail = send_aws(self, request)
		if mail:
			return Response({
                    'status': 'success',
                    'data': {'message': 'Mail Sent Successfully'}
                }, status=status.HTTP_200_OK)
		else:
			return Response({
				'status': 'failure',
				'data': { 'message': 'Incorrect request format.'}
				}, status=status.HTTP_400_BAD_REQUEST)