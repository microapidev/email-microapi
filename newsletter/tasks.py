from celery import shared_task
from time import sleep
from django.core.mail import send_mail


@shared_task
def send_email():
    sleep(10)
    send_mail(subject, body, from_email, [to_email])
    return send_mail

@shared_task
def send_custom_mail():
    sleep(10)
    message = EmailMultiAlternatives(subject, newsletter_mail, from_email, [to_email])
    return message


