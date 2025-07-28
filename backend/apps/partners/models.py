from django.db import models
from django.utils.text import slugify


class PartnerCategory(models.Model):
    """Categorías para los partners/colaboradores"""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='Descripción')
    order = models.IntegerField(default=0, verbose_name='Orden de visualización')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Partner'
        verbose_name_plural = 'Categorías de Partners'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Partner(models.Model):
    """Partners/Colaboradores de Calicanto"""
    
    PARTNER_TYPES = (
        ('company', 'Empresa'),
        ('ngo', 'ONG'),
        ('cooperative', 'Cooperativa'),
        ('foundation', 'Fundación'),
        ('association', 'Asociación'),
        ('public', 'Entidad Pública'),
        ('other', 'Otro'),
    )
    
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    partner_type = models.CharField(
        max_length=20,
        choices=PARTNER_TYPES,
        default='company',
        verbose_name='Tipo de entidad'
    )
    category = models.ForeignKey(
        PartnerCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partners',
        verbose_name='Categoría'
    )
    
    # Descripción y misión
    description = models.TextField(verbose_name='Descripción')
    mission = models.TextField(
        blank=True,
        verbose_name='Misión',
        help_text='Misión o propósito de la organización'
    )
    
    # Información de contacto
    contact_person = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Persona de contacto'
    )
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    website = models.URLField(blank=True, verbose_name='Sitio web')
    
    # Dirección
    address = models.CharField(max_length=200, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    province = models.CharField(max_length=100, verbose_name='Provincia')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Código postal')
    
    # Redes sociales
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    twitter = models.URLField(blank=True, verbose_name='Twitter/X')
    facebook = models.URLField(blank=True, verbose_name='Facebook')
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    
    # Colaboración
    collaboration_areas = models.TextField(
        blank=True,
        verbose_name='Áreas de colaboración',
        help_text='Una por línea. Ej: Arquitectura sostenible, Financiación, etc.'
    )
    collaboration_start = models.DateField(
        null=True,
        blank=True,
        verbose_name='Inicio de colaboración'
    )
    
    # Logotipo e imagen
    logo = models.ImageField(
        upload_to='partners/logos/',
        null=True,
        blank=True,
        verbose_name='Logotipo'
    )
    featured_image = models.ImageField(
        upload_to='partners/images/',
        null=True,
        blank=True,
        verbose_name='Imagen destacada'
    )
    
    # Metadatos
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacado',
        help_text='Mostrar en la página principal'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    order = models.IntegerField(default=0, verbose_name='Orden de visualización')
    
    # Registro
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['-is_featured', 'order', 'name']
        indexes = [
            models.Index(fields=['partner_type', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_location(self):
        """Devuelve la ubicación formateada"""
        return f"{self.city}, {self.province}"

    def get_collaboration_areas_list(self):
        """Devuelve las áreas de colaboración como lista"""
        if self.collaboration_areas:
            return [area.strip() for area in self.collaboration_areas.split('\n') if area.strip()]
        return []

    def get_social_media_links(self):
        """Devuelve un diccionario con los enlaces a redes sociales"""
        links = {}
        if self.linkedin:
            links['linkedin'] = self.linkedin
        if self.twitter:
            links['twitter'] = self.twitter
        if self.facebook:
            links['facebook'] = self.facebook
        if self.instagram:
            links['instagram'] = self.instagram
        return links


class PartnerTestimonial(models.Model):
    """Testimonios de partners"""
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='testimonials',
        verbose_name='Partner'
    )
    author = models.CharField(max_length=100, verbose_name='Autor')
    role = models.CharField(max_length=100, verbose_name='Cargo')
    content = models.TextField(verbose_name='Contenido')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'
        ordering = ['-created_at']

    def __str__(self):
        return f"Testimonio de {self.author} - {self.partner.name}"


class PartnerProject(models.Model):
    """Proyectos realizados con partners"""
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='partner_projects',
        verbose_name='Partner'
    )
    project = models.ForeignKey(
        'proyectos.Project',
        on_delete=models.CASCADE,
        related_name='partner_collaborations',
        verbose_name='Proyecto'
    )
    role = models.CharField(
        max_length=200,
        verbose_name='Rol en el proyecto',
        help_text='Ej: Financiación, Arquitectura, Construcción, etc.'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción de la colaboración'
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de inicio'
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de finalización'
    )
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Colaboración en Proyecto'
        verbose_name_plural = 'Colaboraciones en Proyectos'
        ordering = ['-start_date']
        unique_together = [['partner', 'project']]

    def __str__(self):
        return f"{self.partner.name} - {self.project.name}"