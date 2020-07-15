from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
import os
# from rest_framework_swagger.views import get_swagger_view

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view, SwaggerUIRenderer
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
# schema_view = get_swagger_view(title="Send Email Docs")
SwaggerUIRenderer.template = 'drf-yasg.html'

class SchemaGenerator(OpenAPISchemaGenerator):
	def get_schema(self, request=None, public=False):
		schema = super(SchemaGenerator, self).get_schema(request, public)
		schema.basePath = os.path.join(schema.basePath, '')
		return schema


schema_view = get_schema_view(
	openapi.Info(
		title="Send Mail API",
		default_version='v1',
		description="A simple service for sending emails.",
	),
	public=False,
	generator_class = SchemaGenerator,
	urlconf = "send_email_microservice.urls",
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/documentation/', schema_view.as_view(), {'format': '.json'}, name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include('api.urls')),
    path('v1/', include('awsmail.urls')),
    path('v1/', include('aws_sns.urls')),
	path('v1/', include('registration.urls')),
	path('v1/', include('confirmation.urls')),
	path('v1/', include('invitation.urls')),
	path('v1/', include('newsletter.urls')),
	path('v1/', include('send_certificate.urls')),
	path('v1/', include('scheduler.urls')),
    # path('v1/', include('Greetings_mail.urls')),
	path('bouncy/', include('django_bouncy.urls')),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)