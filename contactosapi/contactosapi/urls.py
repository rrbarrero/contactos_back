"""contactosapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny


urlpatterns = [
    path("admin/", admin.site.urls),
    path(settings.URL_API_PREFIX, include("visago.urls")),
    path(settings.URL_API_PREFIX, include("agenda.urls")),
    path(settings.URL_API_PREFIX, include("listas.urls")),
    path(settings.URL_API_PREFIX, include("mail_templates.urls")),
    path(
        "openapi/",
        get_schema_view(
            title="Contactos backend",
            description="API Backend para la aplicación de Contactos",
        ),
        name="openapi-schema",
    ),
    path(
        "",
        TemplateView.as_view(
            template_name="documentation.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
