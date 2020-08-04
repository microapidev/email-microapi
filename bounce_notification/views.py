import boto3
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.conf import settings
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
        topic_arn = 'arn:aws:sns:eu-west-2:084175886792:Bounces'
        bounce_subscription = sns_connection.subscribe(
                                        TopicArn=topic_arn,
                                        Protocol='email', 
                                        Endpoint='email_address')
        return Response(bounce_subscription)
