from django.contrib import admin
from password_reset.models import ResetPasswordToken

# Register your models here.
@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'ip_address', 'user_agent')
