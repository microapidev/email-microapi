from django.db import models


# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

