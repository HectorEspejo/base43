from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectCategory(models.Model):
    """Categorías para los proyectos de vivienda"""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Nombre del icono o clase CSS'
    )
    order = models.IntegerField(default=0, verbose_name='Orden de visualización')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Proyecto'
        verbose_name_plural = 'Categorías de Proyectos'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Proyectos de vivienda colaborativa"""
    
    STATUS_CHOICES = (
        ('planning', 'Planificación'),
        ('development', 'En desarrollo'),
        ('construction', 'En construcción'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('paused', 'Pausado'),
    )
    
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Categoría'
    )
    
    # Ubicación
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    province = models.CharField(max_length=100, verbose_name='Provincia')
    address = models.CharField(max_length=200, blank=True, verbose_name='Dirección')
    coordinates = models.CharField(
        max_length=100, 
        blank=True,
        help_text='Latitud,Longitud para mostrar en mapa'
    )
    
    # Descripción
    short_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Descripción corta',
        help_text='Para mostrar en tarjetas y listados. Si se deja vacío, se generará automáticamente.'
    )
    description = models.TextField(verbose_name='Descripción completa')
    
    # Características del proyecto
    units = models.IntegerField(
        verbose_name='Número de unidades/viviendas',
        validators=[MinValueValidator(1)]
    )
    participants = models.IntegerField(
        default=0,
        verbose_name='Número de participantes',
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning',
        verbose_name='Estado'
    )
    
    # Fechas
    start_date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Fecha de inicio'
    )
    estimated_completion = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Fecha estimada de finalización'
    )
    
    # Características destacadas
    features = models.TextField(
        blank=True,
        verbose_name='Características',
        help_text='Una por línea. Ej: Eficiencia energética A+, Zonas comunes, etc.'
    )
    
    # Información adicional
    investment_range = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Rango de inversión',
        help_text='Ej: 150.000€ - 200.000€'
    )
    financing_type = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Tipo de financiación'
    )
    
    # Partner/Colaborador
    partner = models.ForeignKey(
        'partners.Partner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='direct_projects',
        verbose_name='Partner/Colaborador principal'
    )
    
    # Imagen principal
    image = models.ImageField(
        upload_to='projects/images/',
        null=True,
        blank=True,
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
    
    # URLs externas
    website = models.URLField(blank=True, verbose_name='Sitio web')
    video_url = models.URLField(
        blank=True, 
        verbose_name='URL del video',
        help_text='YouTube, Vimeo, etc.'
    )
    
    # Registro
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='projects_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-is_featured', 'order', '-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['status', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_location()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Auto-generar short_description si está vacío
        if not self.short_description and self.description:
            # Tomar los primeros 297 caracteres y añadir "..."
            if len(self.description) > 297:
                self.short_description = self.description[:297] + '...'
            else:
                self.short_description = self.description
        
        super().save(*args, **kwargs)

    def get_location(self):
        """Devuelve la ubicación formateada"""
        return f"{self.city}, {self.province}"

    def get_features_list(self):
        """Devuelve las características como lista"""
        if self.features:
            return [f.strip() for f in self.features.split('\n') if f.strip()]
        return []

    def get_status_display_class(self):
        """Devuelve la clase CSS para el badge del estado"""
        status_classes = {
            'planning': 'badge-secondary',
            'development': 'badge-info',
            'construction': 'badge-warning',
            'active': 'badge-success',
            'completed': 'badge-primary',
            'paused': 'badge-ghost'
        }
        return status_classes.get(self.status, 'badge-ghost')


class ProjectImage(models.Model):
    """Imágenes adicionales del proyecto"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Proyecto'
    )
    image = models.ImageField(
        upload_to='projects/gallery/',
        verbose_name='Imagen'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descripción'
    )
    order = models.IntegerField(default=0, verbose_name='Orden')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Imagen del Proyecto'
        verbose_name_plural = 'Imágenes del Proyecto'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Imagen de {self.project.name}"


class ProjectDocument(models.Model):
    """Documentos relacionados con el proyecto"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Proyecto'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    file = models.FileField(
        upload_to='projects/documents/',
        verbose_name='Archivo'
    )
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_public = models.BooleanField(
        default=True,
        verbose_name='Público',
        help_text='¿Visible para todos los usuarios?'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Documento del Proyecto'
        verbose_name_plural = 'Documentos del Proyecto'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.project.name}"


class ProjectUpdate(models.Model):
    """Actualizaciones/noticias del proyecto"""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name='Proyecto'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    image = models.ImageField(
        upload_to='projects/updates/',
        null=True,
        blank=True,
        verbose_name='Imagen'
    )
    is_milestone = models.BooleanField(
        default=False,
        verbose_name='Hito importante',
        help_text='Marcar si es un hito importante del proyecto'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Actualización del Proyecto'
        verbose_name_plural = 'Actualizaciones del Proyecto'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.project.name}"