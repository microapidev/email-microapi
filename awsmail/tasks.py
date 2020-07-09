from celery import shared_task
from django.shortcuts import render
from django.core.mail import send_mail
from time import sleep


@shared_task()
def send_aws(subject, body, sender, recipient):
    send_mail(subject, body, sender, [recipient], fail_silently=False)
    return send_mail()
