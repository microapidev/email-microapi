from celery import shared_task
from time import sleep
from django.core.mail import send_mail, EmailMultiAlternatives


@shared_task
def send_email(subject, body, from_email, [to_email]):
    sleep(10)
    send_mail(subject, body, from_email, [to_email])
    return send_mail

@shared_task
def send_custom_mail(subject, newsletter_mail, from_email, [to_email]):
    sleep(10)
    EmailMultiAlternatives(subject, newsletter_mail, from_email, [to_email])
    return EmailMultiAlternatives


