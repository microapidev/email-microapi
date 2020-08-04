from celery import shared_task
from django.shortcuts import render
from django.core.mail import send_mail
from time import sleep
from django.core.mail import EmailMessage


@shared_task()
def send_aws_mail(subject, body, sender, recipient, tmpl=None):
    send_mail(subject, body, sender, [recipient], html_message=tmpl)
    return

@shared_task()
def send_aws_mail_attachment(subject, body, sender, recipient, attach):
	mail = EmailMessage(subject, body, sender, [recipient])
	mail.attach(attach.name, attach.read(), attach.content_type)
	return mail.send()

