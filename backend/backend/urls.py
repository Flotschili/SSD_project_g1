"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import urls as auth_urls
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse, path, include
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import BasePermission  # Import this
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from drf_yasg import openapi

class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if settings.DEBUG:
                return False
            return False
        return request.user.is_staff

def swagger_redirect(request):
    if not request.user.is_authenticated and settings.DEBUG:
        login_url = f"/auth/login/?next={request.path}"
        return HttpResponseRedirect(login_url)  # Redirect to /auth/api/login/ with ?next=/swagger/
    return schema_view.with_ui('swagger', cache_timeout=0)(request)


API_TITLE = 'BeerHub'
API_DESCRIPTION = 'A nice web API for beer'

schema_view = swagger_get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version='v1',
        description=API_DESCRIPTION
    ),
    public=True,
    permission_classes=(AdminOnlyPermission,),
)

urlpatterns = [
    path('admin-kelRtItCHrav/', admin.site.urls),

    path('schema/', get_schema_view(title=API_TITLE)),

    path('swagger/', swagger_redirect, name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('auth/', include('rest_framework.urls')),
    path('api/v1/beers/', include('beers.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
]
