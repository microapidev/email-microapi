from django.urls import path
from .views import AwsMail

urlpatterns = [
    path('awsmail/', AwsMailView.as_view()),
    path('awsmail-attachment/', AwsMailAttachmentView.as_view())
]