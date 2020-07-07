from django.contrib import admin
from .models import Newsletter


class NewsletterEmail(admin.ModelAdmin):
    list_display = ('subject', 'body', 'status', 'created', 'updated')


admin.site.register(Newsletter, NewsletterEmail)

