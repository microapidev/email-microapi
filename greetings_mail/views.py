from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import GreetingsBC
from .serializers import GreetingsSerializer
# Create your views here.


BC_RESPONSES = {
    '200': 'GET request successful',
    '500': 'An error occurred, request could not be completed.'
}

class GreetingsApiView(generics.ListAPIView):
    serializer_class = GreetingsSerializer

    def get_queryset(self):
        #pass in a url param
        parm = self.request.GET.get('type')
        if parm:
            queryset = GreetingsBC.objects.filter(message_type=parm)
        else:
            queryset = GreetingsBC.objects.all()
        
        return queryset

    @swagger_auto_schema(
        operation_summary="an end point that supplies a list of curated email broadcasts",
        operation_description="Provides a list of email broadcasts to pick from, for new year/month, or general greetings, you can pass in three types of url parameters \n to filter the list, i.e http://127.0.0.1:8000/v1/greetings?type=general, where type can also be new month or new year. ",
        responses=BC_RESPONSES
    )
    def get(self, request):
        prit = GreetingsSerializer(self.get_queryset(), many=True)
        lst = prit.data
        return Response(lst)