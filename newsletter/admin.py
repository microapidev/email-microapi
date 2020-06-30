from django.contrib import admin
from .models import Subscriber, Newsletter, NewsletterTemplate


class NewsletterSubscriber(admin.ModelAdmin):
    list_display = ('email', 'date_added')


admin.site.register(Subscriber, NewsletterSubscriber)


class NewsletterEmail(admin.ModelAdmin):
    list_display = ('subject', 'body', 'status', 'created', 'updated')


admin.site.register(Newsletter, NewsletterEmail)


class TemplateHolder(admin.ModelAdmin):
    list_display = ['title', 'html_template']


admin.site.register(NewsletterTemplate,)
