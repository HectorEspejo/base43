from django.db import models
from django.conf import settings
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """Categorías para los servicios ofrecidos"""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(
        max_length=100, 
        blank=True, 
        help_text='Nombre del icono o clase CSS (ej: architecture, construction, legal)'
    )
    color = models.CharField(
        max_length=20, 
        default='primary',
        help_text='Color del tema (primary, secondary, accent, etc.)'
    )
    order = models.IntegerField(default=0, verbose_name='Orden de visualización')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Servicio'
        verbose_name_plural = 'Categorías de Servicios'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Servicios ofrecidos en la plataforma"""
    
    PRICE_TYPES = (
        ('fixed', 'Precio Fijo'),
        ('hourly', 'Por Hora'),
        ('project', 'Por Proyecto'),
        ('consultation', 'Consulta Gratuita'),
        ('quote', 'Bajo Presupuesto'),
    )
    
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre del Servicio')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        related_name='services',
        verbose_name='Categoría'
    )
    description = models.TextField(verbose_name='Descripción')
    short_description = models.CharField(
        max_length=300, 
        blank=True,
        verbose_name='Descripción corta',
        help_text='Para mostrar en tarjetas y listados'
    )
    
    # Detalles del servicio
    features = models.TextField(
        blank=True,
        verbose_name='Características',
        help_text='Lista de características separadas por líneas'
    )
    requirements = models.TextField(
        blank=True,
        verbose_name='Requisitos',
        help_text='Requisitos o documentación necesaria'
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Duración estimada',
        help_text='Ej: 2-3 semanas, 1 mes, Variable'
    )
    
    # Precios
    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPES,
        default='quote',
        verbose_name='Tipo de precio'
    )
    price_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio mínimo'
    )
    price_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio máximo'
    )
    price_note = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nota sobre el precio',
        help_text='Ej: IVA no incluido, Precio por m²'
    )
    
    # Proveedor/Profesional
    provider_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre del proveedor'
    )
    provider_email = models.EmailField(
        blank=True,
        verbose_name='Email de contacto'
    )
    provider_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono de contacto'
    )
    provider_website = models.URLField(
        blank=True,
        verbose_name='Sitio web'
    )
    
    # Imágenes
    image = models.ImageField(
        upload_to='services/images/',
        blank=True,
        null=True,
        verbose_name='Imagen principal'
    )
    
    # Metadatos
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacado',
        help_text='Mostrar en la página principal'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    order = models.IntegerField(default=0, verbose_name='Orden de visualización')
    views = models.IntegerField(default=0, verbose_name='Vistas')
    
    # Registro
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='services_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['category', 'order', 'name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.category.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_features_list(self):
        """Devuelve las características como lista"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def get_price_display(self):
        """Devuelve el precio formateado"""
        if self.price_type == 'consultation':
            return 'Consulta Gratuita'
        elif self.price_type == 'quote':
            return 'Bajo Presupuesto'
        elif self.price_min and self.price_max:
            return f'€{self.price_min} - €{self.price_max}'
        elif self.price_min:
            return f'Desde €{self.price_min}'
        return 'Consultar precio'


class ServiceInquiry(models.Model):
    """Consultas sobre servicios"""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='inquiries',
        verbose_name='Servicio'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    message = models.TextField(verbose_name='Mensaje')
    
    # Estado
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    is_answered = models.BooleanField(default=False, verbose_name='Respondido')
    notes = models.TextField(blank=True, verbose_name='Notas internas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_inquiries_answered'
    )

    class Meta:
        verbose_name = 'Consulta de Servicio'
        verbose_name_plural = 'Consultas de Servicios'
        ordering = ['-created_at']

    def __str__(self):
        return f"Consulta de {self.name} sobre {self.service.name}"