from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
import os
from .views import SettingsView
# from .views import ReturnSettings
# from rest_framework_swagger.views import get_swagger_view

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import SwaggerUIRenderer,get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
import json
from django.http import JsonResponse
# schema_view = get_swagger_view(title="Send Email Docs")
SwaggerUIRenderer.template = 'drf-yasg.html'

with open(r'swagger\swagger.json') as doc:
	data = doc.read()
data = json.loads(data)
def documentation_func(request):
	return JsonResponse(data,safe=False)

class SchemaGenerator(OpenAPISchemaGenerator):
	def get_schema(self):
		
		# schema = super(SchemaGenerator, self).get_schema(request, public)
		# schema.basePath = os.path.join(schema.basePath, '')
		return schema


schema_view = get_schema_view(
	openapi.Info(
		title="Send Mail API",
		default_version='v1',
		description="A Microservice for Sending Emails.",
	),
	public=True,
	url='https://email.microapi.dev/v1/',
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/documentation/', documentation_func, name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include('api.urls')),
    path('v1/', include('awsmail.urls')),
    path('v1/', include('info.urls')),
	path('v1/', include('registration.urls')),
	path('v1/', include('confirmation.urls')),
	path('v1/', include('invitation.urls')),
	path('v1/', include('newsletter.urls')),
	path('v1/', include('send_certificate.urls')),
	path('v1/bouncy/', include('django_bouncy.urls')),
    path('v1/', include('greetings_mail.urls')),
	path('v1/', include('scheduler.urls')),
    	# path('v1/', include('Greetings_mail.urls')),
	# path('bouncy/', include('django_bouncy.urls')),
	# path('v1/', include('bounce_notification.urls')),
	path('v1/', include('newsletter_with_frontend.urls')),
	path('v1/settings/', SettingsView.as_view()),
	#path('v1/test_settings/', test_settings.as_view()),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
