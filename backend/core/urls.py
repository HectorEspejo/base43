"""
URL configuration for Base43 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Base43 API",
        default_version='v1',
        description="API para la plataforma web Base43",
        terms_of_service="https://www.base43.org/terms/",
        contact=openapi.Contact(email="contact@base43.org"),
        license=openapi.License(name="Copyleft License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1 URLs
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/oferta/', include('apps.oferta.urls')),
    path('api/v1/repositorio/', include('apps.repositorio.urls')),
    path('api/v1/proyectos/', include('apps.proyectos.urls')),
    path('api/v1/noticias/', include('apps.noticias.urls')),
    path('api/v1/chat/', include('apps.chat.urls')),
    path('api/v1/partners/', include('apps.partners.urls')),
    path('api/v1/contacto/', include('apps.contacto.urls')),
    path('api/v1/recursos/', include('apps.recursos.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)