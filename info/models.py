from django.db import models

class Info(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	logo = models.FileField(upload_to='', null=False, blank=False)

