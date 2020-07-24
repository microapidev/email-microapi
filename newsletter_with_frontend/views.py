from django.shortcuts import render
from .models import UserProfile
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .serializer import UserProfileSerializers, EditSerializer



@swagger_auto_schema(
    request_body=UserProfileSerializers,
    operation_description="Gets User Profile and Contents.",
    tags=['Gets User Profile and Contents']
	
@api_view(['GET'])
def profile_list(request):

    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserProfileSerializers(users, many=True)
        return Response(serializer.data)


@swagger_auto_schema(
    request_body=UserProfileSerializers,
    operation_description="Gets, PUTS and DELETE User Profile and Contents.",
    tags=['Gets User Profile and Contents']

@api_view(['GET', 'PUT', 'DELETE'])
def get_user_profile(request, pk):
    try:
        user = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializers(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EditSerializer(user, data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data.get("subject")
            content = serializer.validated_data.get("content")
            recipient = serializer.validated_data.get("recipient")
            sender = settings.EMAIL_HOST_USER
            send_mail(subject, content, sender, [recipient])
            serializer.save()
            return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
