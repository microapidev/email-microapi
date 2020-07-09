from celery import shared_task
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from api.serializers import MailSerializer
from django.core.mail import send_mail
from time import sleep


@shared_task()
def send_aws(subject, body, sender, recipient):
    return send_mail(subject, body, sender, [recipient], fail_silently=False)
