from django.db import models
from django.conf import settings

class ResourceCategory(models.Model):
    """Categorías para los recursos"""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=50, blank=True, help_text='Nombre del icono (ej: home, building)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Recurso'
        verbose_name_plural = 'Categorías de Recursos'
        ordering = ['name']

    def __str__(self):
        return self.name


class Resource(models.Model):
    """Modelo principal para recursos, instituciones y organizaciones"""
    
    RESOURCE_TYPES = (
        ('institucion', 'Institución'),
        ('organizacion', 'Organización'),
        ('servicio', 'Servicio'),
        ('programa', 'Programa'),
        ('cooperativa', 'Cooperativa'),
        ('empresa', 'Empresa'),
        ('otro', 'Otro'),
    )
    
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre')
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES, verbose_name='Tipo')
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, verbose_name='Categoría')
    description = models.TextField(verbose_name='Descripción')
    
    # Ubicación
    address = models.CharField(max_length=300, verbose_name='Dirección')
    city = models.CharField(max_length=100, verbose_name='Ciudad', help_text='Nombre de la ciudad')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Código Postal')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='Latitud')
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name='Longitud')
    
    # Contacto
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Sitio Web')
    
    # Información adicional
    schedule = models.TextField(blank=True, verbose_name='Horario', help_text='Horario de atención')
    services = models.TextField(blank=True, verbose_name='Servicios', help_text='Lista de servicios separados por comas')
    requirements = models.TextField(blank=True, verbose_name='Requisitos', help_text='Requisitos para acceder al recurso')
    
    # Metadatos
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_featured = models.BooleanField(default=False, verbose_name='Destacado')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='resources_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['-is_featured', 'name']
        indexes = [
            models.Index(fields=['city', 'type']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"
    
    def get_services_list(self):
        """Devuelve los servicios como una lista"""
        if self.services:
            return [s.strip() for s in self.services.split(',')]
        return []
    
    @property
    def full_address(self):
        """Devuelve la dirección completa"""
        parts = [self.address]
        if self.postal_code:
            parts.append(self.postal_code)
        if self.city:
            parts.append(self.city)
        return ', '.join(parts)


class ResourceImage(models.Model):
    """Imágenes asociadas a los recursos"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recursos/images/', verbose_name='Imagen')
    caption = models.CharField(max_length=200, blank=True, verbose_name='Descripción')
    is_main = models.BooleanField(default=False, verbose_name='Imagen Principal')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagen de Recurso'
        verbose_name_plural = 'Imágenes de Recursos'
        ordering = ['-is_main', '-created_at']
    
    def __str__(self):
        return f"Imagen de {self.resource.name}"


class ResourceDocument(models.Model):
    """Documentos asociados a los recursos"""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200, verbose_name='Título')
    file = models.FileField(upload_to='recursos/documents/', verbose_name='Archivo')
    description = models.TextField(blank=True, verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Documento de Recurso'
        verbose_name_plural = 'Documentos de Recursos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.resource.name}"