from django.db import models

class Settings(models.Model):
	sender = models.CharField(max_length=200, unique=True, blank=False, null=True)
	backend_type = models.CharField(max_length=200, blank=False, null=True)
	sg_api_key = models.CharField(max_length=225, blank=True, null=True)
	access_key_id = models.CharField(max_length=255, blank=True, null=True)
	secret_access_key = models.CharField(max_length=255, blank=True, null=True)
	region_name = models.CharField(max_length=255, blank=True, null=True)
	region_endpoint = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.sender
		


