from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import MailSerializer
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from rest_framework import status
from awsmail.tasks import send_aws

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
		operation_description="Send email using AMAZON SES",
		operation_summary="Sending email with AMAZON SES",
		responses=MAIL_RESPONSES,
		tags=['Email with Amazon ses']
	)
	def post(self, request, *args, **kwargs):
		serializer = MailSerializer(data=request.data)
		if serializer.is_valid():
			subject = serializer.validated_data.get('subject')
			body = serializer.validated_data.get('body')
			sender = serializer.validated_data.get('sender')
			recipient = serializer.validated_data.get('recipient')

			send_aws.delay(subject, body, sender, recipient)
			
			return Response({
                    'status': 'success',
                    'data': {'message': 'Mail Sent Successfully'}
                }, status=status.HTTP_200_OK)
		else:
			return Response({
				'status': 'failure',
				'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
				}, status=status.HTTP_400_BAD_REQUEST)