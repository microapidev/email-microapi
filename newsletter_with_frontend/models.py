from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=120, default='')
    sender = models.CharField(max_length=120, default='')
    recipient = models.CharField(max_length=250, default='')
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


