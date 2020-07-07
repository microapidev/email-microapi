from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from password_reset.tokens import get_token_generator

# Create your models here.

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# get the token generator class
TOKEN_GENERATOR_CLASS = get_token_generator()

__all__ = [
    'ResetPasswordToken',
    'get_password_reset_token_expiry_time',
    'get_password_reset_lookup_field',
    'clear_expired',
] 


class ResetPasswordToken(models.Model):
    class Meta:
        verbose_name = _("Password Reset Token")
        verbose_name_plural = _("Password Reset Tokens")

        @staticmethod
        def generate_key():
            #generates a pseudorandom code
            return TOKEN_GENERATOR_CLASS.generate_token()

        id = models.AutoField(
            primary_key=True
        )

        user = models.ForeignKey(
            AUTH_USER_MODEL,
            related_name='password_reset_tokens',
            on_delete=models.CASCADE,
            verbose_name=_("The User associated to this password reset token")
        )

        created_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name=_("When this token was generated")
        )

        #Key field with a maximum character length of 64
        key = models.CharField(
            _("Key"),
            max_length=64,
            db_index=True,
            unique=True
        )

        ip_address = models.GenericIPAddressField(
            _("The IP address of this session"),
            default="",
            blank=True,
            null=True,
        )

        user_agent = models.CharField(
            max_length=256,
            verbose_name=_("HTTP User Agent"),
            default="",
            blank=True,
        )

        def save(self, *args, **kwargs):
            if not self.key:
                self.key = self.generate_key()
            return super(self, ResetPasswordToken).save(*args, **kwargs)

        def __str__(self):
            return "Password reser token for user {user}".format(user=self.user)
        
    
    def get_password_reset_token_expiry_time():
        #returns the password reset token expiry token in hours (default: 24)
        return getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME', 24)

    def get_password_reset_lookup_field():
        #returns the password lookup field, which is currently the email address
        return getattr(settings, 'DJANGO_REST_LOOKUP_FIELD', 'email')

    def clear_expired(self, expiry_time):
        #remove all expired tokens
        ResetPasswordToken.objects.filter(created_at__lte=expiry_time).delete()

    def eligible_for_reset(self):
        if not self.is_active:
            #this makes sure the user is online when the password is reset
            return False

        if getattr(settings, 'DJANGO_REST_MULTITOKENAUTH_REQUIRE_USABLE_PASSWORD', True):
            #we use this if we require a usable password then return the result of has_usable_password
            return self.has_usable_password()
        else:
            #otherwise return  True because we don't care about the result of has_usable_password
            return True

    
    UserModel = get_user_model()
    UserModel.add_to_class("eligible_for_reset", eligible_for_reset)
