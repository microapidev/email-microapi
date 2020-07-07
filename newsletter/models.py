from django.db import models


# Create your models here.

class Newsletter(models.Model):
    EMAIL_CHOICE = [
        ('draft', 'draft'),
        ('Published', 'Published')
    ]
    to_email = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    is_html = models.BooleanField(default=False)
    is_plaintxt = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=EMAIL_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.subject

