from django.shortcuts import render
from wsgiref.util import FileWrapper
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status, viewsets
from .serializers import InfoSerializer
from .models import Info

class InfoViewSet(viewsets.ModelViewSet):
	queryset = Info.objects.all()
	serializer_class = InfoSerializer