# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class NewsPost(models.Model):
    """Model for news posts with rich text content and media support."""
    
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    slug = models.SlugField(
        max_length=200,
        unique_for_date='created_at',
        blank=True,
        verbose_name='URL amigable'
    )
    content = RichTextUploadingField(
        verbose_name='Contenido'
    )
    excerpt = models.TextField(
        max_length=500,
        help_text='Resumen breve del artículo para mostrar en la lista',
        verbose_name='Extracto'
    )
    header_image = models.ImageField(
        upload_to='news/headers/%Y/%m/',
        verbose_name='Imagen de cabecera',
        help_text='Imagen principal del artículo (recomendado: 1200x600px)'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='news_posts',
        verbose_name='Autor'
    )
    category = models.CharField(
        max_length=50,
        default='General',
        verbose_name='Categoría',
        choices=[
            ('General', 'General'),
            ('Cooperativas', 'Cooperativas'),
            ('Recursos', 'Recursos'),
            ('Eventos', 'Eventos'),
            ('Legal', 'Legal'),
            ('Proyectos', 'Proyectos'),
            ('Sostenibilidad', 'Sostenibilidad'),
        ]
    )
    published = models.BooleanField(
        default=False,
        verbose_name='Publicado'
    )
    featured = models.BooleanField(
        default=False,
        verbose_name='Destacado',
        help_text='Marcar como noticia destacada'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='Vistas'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'published']),
            models.Index(fields=['slug', 'created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug for the same date
            if NewsPost.objects.filter(
                slug=self.slug,
                created_at__date=self.created_at.date()
            ).exclude(pk=self.pk).exists():
                # Add a number to make it unique
                num = 1
                while NewsPost.objects.filter(
                    slug=f"{self.slug}-{num}",
                    created_at__date=self.created_at.date()
                ).exclude(pk=self.pk).exists():
                    num += 1
                self.slug = f"{self.slug}-{num}"
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/noticias/{self.created_at.year}/{self.created_at.month:02d}/{self.created_at.day:02d}/{self.slug}/"
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])