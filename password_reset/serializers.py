from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

from rest_framework import serializers

__all__ = [
    'EmailSerializer',
    'PasswordTokenSerializer',
    'TokenSerializer',
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not UserModel.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'example_message.txt',
            'html_email_template_name': 'account/email/example_message.html',
            

            'request': request,
        }
        self.reset_form.save(**opts)