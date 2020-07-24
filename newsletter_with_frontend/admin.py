from django.contrib import admin
from .models import UserProfile


class AdminUserProfile(admin.ModelAdmin):
    list_display = [
        "user",
        "content",
        'sender',
        "subject",
        "recipient",
        "created",
    ]


admin.site.register(UserProfile, AdminUserProfile)
