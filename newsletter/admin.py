from django.contrib import admin
from .models import Newsletter


class NewsletterEmail(admin.ModelAdmin):
    list_display = ('subject', 'body', 'from_email', 'to_email', 'created')


admin.site.register(Newsletter, NewsletterEmail)

