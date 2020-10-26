import boto3
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.conf import settings
from .serializer import BounceSerializer
from drf_yasg.utils import swagger_auto_schema

class BounceNotification(APIView):
    """Receives a bounce notification from Amazon SNS"""
    @swagger_auto_schema(
		operation_description="Receives bounce notifications.",
        tags=['Bounce Notification']
	)
    def post(self, request):
        #Creates a connection to AWS.
        sns_connection = boto3.client('sns', region_name=settings.AWS_SES_REGION_NAME,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        
        #Creates an SNS topic to be subscribed to
        sns_topic_object = sns_connection.create_topic('Bounces')
        
                
        #Creates an SNS subcription that receives messages published to the topic above
        #insert the topic arn name gotten from creating the topic above.
        #Protocol could be HTTP(S), email, and/or mobile app

        serializer = BounceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic_arn = serializer.validated_data["topic_arn"]
        subscriber_email = serializer.validated_data["subscriber_email"]
        bounce_subscription = sns_connection.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=subscriber_email
        )
        return Response(bounce_subscription)
