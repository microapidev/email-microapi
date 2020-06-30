from django.db import models


# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    EMAIL_CHOICE = [
        ('draft', 'draft'),
        ('Published', 'Published')
    ]
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    email = models.EmailField(max_length=245, default="Not Null")
    status = models.CharField(max_length=10, choices=EMAIL_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class NewsletterTemplate(models.Model):
    title = models.CharField(max_length=250)
    html_template = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title
