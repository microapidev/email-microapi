from celery import shared_task
from django.shortcuts import render
from sendgrid import SendGridAPIClient
from send_email_microservice.settings import SENDGRID_API_KEY
from sendgrid.helpers.mail import *
from time import sleep


@shared_task()
def send_mail(sender, recipient, subject, content):

    sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)

    mail = Mail(sender, recipient, subject, content)

    send = sg.send(mail)

    return send
