from celery import shared_task
from django.shortcuts import render
from django.core.mail import send_mail
from time import sleep
from api.views import send_email


@shared_task()
def send_grid():
    send_email(options, is_html_template=False)
    sleep(5)
    return send_email()
