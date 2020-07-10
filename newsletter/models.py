from django.db import models

# Create your models here.
class Newsletter(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=500)
    body = models.TextField()
    from_email = models.EmailField(default='')
    to_email = models.EmailField(default='')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject

