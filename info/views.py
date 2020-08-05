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
	url = "https://email-microdev.herokuapp.com"
	parser_classes = [FileUploadParser, MultiPartParser]

	def get(self, request, format=None, *args, **kwargs):
		queryset = Info.objects.all()
		serializer = InfoSerializer(queryset, many=True)
		for data in serializer.data:
			title = data['title']
			description = data['description']
			icon = data['icon']

			return Response({
						"message": "info retreived successfully!",
						"data": {
							"title": title, 
							"description": description, 
							"icon": url+icon
						},
						"success": True
					}, status=status.HTTP_200_OK)
		return Response({"message": "info couldn\'t be retreived!", "success": False}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request, *args, **kwargs):
		serializer = InfoSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response({
						"message": "info updated successfully!",
						"data": {
							"title": serializer.data['title'], 
							"description": serializer.data['description'], 
							"icon": url+serializer.data['icon']
						}
						"success": True,
					}, status=status.HTTP_200_OK)
		return Response({
						"message": "bad request!", 
						"errors": serializer.errors,
						"success": False,
					}, status=status.HTTP_400_BAD_REQUEST)