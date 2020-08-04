from django.shortcuts import render
from django.http import JsonResponse
from wsgiref.util import FileWrapper
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from .serializers import InfoSerializer
from .models import Info

class InfoView(APIView):

	parser_classes = [FileUploadParser, MultiPartParser]

	def get(self, request, format=None, *args, **kwargs):
		queryset = Info.objects.all()
		serializer = InfoSerializer(queryset, many=True)
		for data in serializer.data:
			title = data['title']
			description = data['description']
			icon = data['icon']

			return Response({
						"status": "success",
						"data":{
							"title": title, 
							"description": description, 
							"icon": "https://email-microdev.herokuapp.com"+icon
						}
					}, status=status.HTTP_200_OK)
		return Response({"status": "info request failed"}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, *args, **kwargs):
		serializer = InfoSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({
						"status": "success",
						"data":{
							"message": "info updated successfully",
							"title": serializer.data['title'], 
							"description": serializer.data['description'], 
							"icon": "https://email-microdev.herokuapp.com"+serializer.data['icon']
						}
					}, status=status.HTTP_200_OK)
		return Response({
						"status": "failure",
						"data":{
							"message": "bad request", 
							"errors": serializer.errors
						}
					}, status=status.HTTP_400_BAD_REQUEST)