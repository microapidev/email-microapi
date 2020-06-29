from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import MailSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.core.mail import send_mail

MAIL_RESPONSES = {
	'200': 'Mail sent successfully.',
	'400': 'Incorrect request format.',
	'500': 'An error occurred, could not send email.' 
}

"""
Send email using AWS Simple Email Service (SES)
"""

class awsMail(APIView):
	@swagger_auto_schema(
		request_body=MailSerializer,
		operation_description="Send email using SES from AWS.",
		operation_summary="Sending email with amazon ses",
		responses=MAIL_RESPONSES
		)

	def post(self, request):
		serializer = MailSerializer(data=request.data)
		if serializer.is_valid():
			subject = serializer.validated_data.get('subject')
			message = serializer.validated_data.get('body')
			from_email = serializer.validated_data.get('sender')
			recipient_list = serializer.validated_data.get('recipient')

			response = send_mail(subject,message,from_email,[recipient_list])

			return Response({
                    'status': 'success',
                    'data': {'message': 'Invitation Sent Successfully'}
                }, status=status.HTTP_200_OK)

		else:
			return Response({
				'status': 'failure',
				'data': { 'message': 'Incorrect request format.', 'errors': serializer.errors}
			}, status=status.HTTP_400_BAD_REQUEST)


