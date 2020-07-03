'''from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

from django.conf.urls import url, include
from password_reset.views import reset_password_request_token, reset_password_confirm, reset_password_validate_token

urlpatterns = [
    #path('sendmail/', views.SendMail.as_view()),
    url(r'^validate_token/', reset_password_validate_token, name="reset-password-validate"),
    url(r'^confirm/', reset_password_confirm, name="reset-password-confirm"),
    url(r'^', reset_password_request_token, name="reset-password-request"),
]
'''
