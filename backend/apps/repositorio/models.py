# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import os
import mimetypes

User = get_user_model()


def validate_file_size(file):
    """Validate that file size is not greater than 50MB."""
    limit = 50 * 1024 * 1024  # 50MB
    if file.size > limit:
        raise ValidationError('El archivo no puede superar los 50MB.')


class Category(models.Model):
    """Main categories for the repository."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Nombre del icono (ej: folder-open)',
        verbose_name='Icono'
    )
    order = models.IntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización (menor número aparece primero)'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Directory(models.Model):
    """Directories within categories."""
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='directories',
        verbose_name='Categoría'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subdirectories',
        verbose_name='Directorio padre'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_directories',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Público',
        help_text='Si está desmarcado, solo usuarios registrados pueden acceder'
    )
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='allowed_directories',
        verbose_name='Usuarios permitidos',
        help_text='Dejar vacío para permitir a todos los usuarios registrados'
    )
    
    class Meta:
        verbose_name = 'Directorio'
        verbose_name_plural = 'Directorios'
        ordering = ['name']
        unique_together = [['name', 'parent', 'category']]
    
    def __str__(self):
        if self.parent:
            return f"{self.parent} / {self.name}"
        return f"{self.category.name} / {self.name}"
    
    def get_full_path(self):
        """Get the full path of the directory."""
        if self.parent:
            return f"{self.parent.get_full_path()}/{self.name}"
        return self.name
    
    def get_all_files(self):
        """Get all files in this directory and subdirectories."""
        files = list(self.files.all())
        for subdir in self.subdirectories.all():
            files.extend(subdir.get_all_files())
        return files


def repository_file_path(instance, filename):
    """Generate file path for repository files."""
    # Clean filename
    name, ext = os.path.splitext(filename)
    clean_name = slugify(name)
    if not clean_name:
        clean_name = 'archivo'
    filename = f"{clean_name}{ext}"
    
    # Build path
    if instance.directory:
        path_parts = ['repositorio', instance.category.slug, instance.directory.get_full_path(), filename]
    else:
        path_parts = ['repositorio', instance.category.slug, filename]
    
    return os.path.join(*path_parts)


class RepositoryFile(models.Model):
    """Files in the repository."""
    LICENSE_CHOICES = [
        ('CC0', 'CC0 - Dominio Público'),
        ('CC-BY', 'CC BY - Atribución'),
        ('CC-BY-SA', 'CC BY-SA - Atribución-CompartirIgual'),
        ('CC-BY-NC', 'CC BY-NC - Atribución-NoComercial'),
        ('CC-BY-NC-SA', 'CC BY-NC-SA - Atribución-NoComercial-CompartirIgual'),
        ('Apache-2.0', 'Apache License 2.0'),
        ('MIT', 'MIT License'),
        ('GPL-3.0', 'GPL v3.0'),
        ('Copyleft', 'Copyleft'),
        ('Copyright', 'Copyright - Todos los derechos reservados'),
        ('Other', 'Otra licencia'),
    ]
    
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre'
    )
    file = models.FileField(
        upload_to=repository_file_path,
        validators=[validate_file_size],
        verbose_name='Archivo'
    )
    directory = models.ForeignKey(
        Directory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='files',
        verbose_name='Directorio'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Categoría'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    license = models.CharField(
        max_length=20,
        choices=LICENSE_CHOICES,
        default='CC-BY-SA',
        verbose_name='Licencia'
    )
    size = models.BigIntegerField(
        editable=False,
        verbose_name='Tamaño (bytes)'
    )
    mime_type = models.CharField(
        max_length=100,
        editable=False,
        verbose_name='Tipo MIME'
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files',
        verbose_name='Subido por'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de subida'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última modificación'
    )
    downloads = models.PositiveIntegerField(
        default=0,
        verbose_name='Descargas'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Público',
        help_text='Si está desmarcado, solo usuarios registrados pueden acceder'
    )
    is_hidden = models.BooleanField(
        default=False,
        verbose_name='Oculto',
        help_text='Los archivos ocultos no se muestran en el listado'
    )
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='allowed_files',
        verbose_name='Usuarios permitidos',
        help_text='Dejar vacío para permitir a todos los usuarios registrados'
    )
    
    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'directory']),
            models.Index(fields=['uploaded_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Set file size
        if self.file:
            self.size = self.file.size
            
            # Set mime type
            mime_type, _ = mimetypes.guess_type(self.file.name)
            self.mime_type = mime_type or 'application/octet-stream'
        
        super().save(*args, **kwargs)
    
    def get_extension(self):
        """Get file extension."""
        if not self.name:
            return ''
        # Try to get extension from name first
        ext = os.path.splitext(self.name)[1][1:].upper()
        # If no extension in name, try from file field
        if not ext and self.file:
            ext = os.path.splitext(self.file.name)[1][1:].upper()
        return ext
    
    def get_icon(self):
        """Get icon based on file type."""
        ext = self.get_extension().lower()
        
        # Image files
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp']:
            return 'image'
        # Documents
        elif ext in ['pdf']:
            return 'pdf'
        elif ext in ['doc', 'docx']:
            return 'word'
        elif ext in ['xls', 'xlsx']:
            return 'excel'
        elif ext in ['ppt', 'pptx']:
            return 'powerpoint'
        # Archives
        elif ext in ['zip', 'rar', '7z', 'tar', 'gz']:
            return 'archive'
        # Code
        elif ext in ['py', 'js', 'html', 'css', 'java', 'cpp', 'c']:
            return 'code'
        # Text
        elif ext in ['txt', 'md']:
            return 'text'
        else:
            return 'file'
    
    def can_preview(self):
        """Check if file can be previewed."""
        if not self.name:
            return False
        ext = self.get_extension().lower()
        return ext in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'pdf', 'txt', 'md']
    
    def increment_downloads(self):
        """Increment download counter."""
        self.downloads += 1
        self.save(update_fields=['downloads'])
    
    def check_permission(self, user):
        """Check if user has permission to access this file."""
        # Hidden files are only visible to staff
        if self.is_hidden and (not user or not user.is_authenticated or not user.is_staff):
            return False
        
        # Public files are accessible to everyone
        if self.is_public:
            return True
        
        # Non-public files require authentication
        if not user or not user.is_authenticated:
            return False
        
        # Check specific user permissions
        if self.pk and self.allowed_users.exists():
            return self.allowed_users.filter(id=user.id).exists()
        
        # If no specific users, any authenticated user can access
        return True