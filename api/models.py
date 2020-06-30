from django.db import models

# Create your models here.
class GreetingsBC(models.Model):
    text = models.TextField()
    message_type = models.CharField(max_length=100)