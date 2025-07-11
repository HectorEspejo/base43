# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
import os

User = get_user_model()


def validate_file_size(file):
    """Validate that file size is not greater than 20MB."""
    limit = 20 * 1024 * 1024  # 20MB
    if file.size > limit:
        raise ValidationError('El archivo no puede superar los 20MB.')


class Channel(models.Model):
    """Model for chat channels."""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nombre'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_channels',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        verbose_name = 'Canal'
        verbose_name_plural = 'Canales'
        ordering = ['name']
    
    def __str__(self):
        return f"#{self.name}"
    
    def get_online_users(self):
        """Get users currently online in this channel."""
        # This will be implemented with WebSocket tracking
        return User.objects.none()
    
    def get_member_count(self):
        """Get total number of members who have sent messages in this channel."""
        return self.messages.values('user').distinct().count()


def message_file_path(instance, filename):
    """Generate file path for message attachments."""
    ext = filename.split('.')[-1]
    filename = f"{instance.user.id}_{timezone.now().timestamp()}.{ext}"
    return os.path.join('chat', str(instance.channel.id), filename)


class Message(models.Model):
    """Model for chat messages."""
    FILE_TYPE_CHOICES = [
        ('image', 'Imagen'),
        ('document', 'Documento'),
    ]
    
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Canal'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='chat_messages',
        verbose_name='Usuario'
    )
    content = models.TextField(
        blank=True,
        verbose_name='Contenido',
        help_text='Contenido del mensaje con formato Markdown'
    )
    file = models.FileField(
        upload_to=message_file_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'xlsx', 'doc', 'xls']
            ),
            validate_file_size
        ],
        verbose_name='Archivo adjunto'
    )
    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES,
        blank=True,
        verbose_name='Tipo de archivo'
    )
    file_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Nombre del archivo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de envío'
    )
    edited_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de edición'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Eliminado'
    )
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['channel', '-created_at']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name() if self.user else 'Usuario eliminado'} en {self.channel.name}: {self.content[:50]}"
    
    def save(self, *args, **kwargs):
        # Determine file type based on extension
        if self.file and not self.file_type:
            ext = self.file.name.split('.')[-1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'gif']:
                self.file_type = 'image'
            else:
                self.file_type = 'document'
        
        # Store original filename
        if self.file and not self.file_name:
            self.file_name = os.path.basename(self.file.name)
        
        super().save(*args, **kwargs)
    
    def soft_delete(self):
        """Soft delete the message."""
        self.is_deleted = True
        self.content = "[Mensaje eliminado]"
        self.file = None
        self.save()
    
    def get_file_url(self):
        """Get the full URL for the file."""
        if self.file:
            return self.file.url
        return None


class ChannelMembership(models.Model):
    """Track user membership and read status in channels."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='channel_memberships',
        verbose_name='Usuario'
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Canal'
    )
    last_read_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Última lectura'
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de unión'
    )
    
    class Meta:
        verbose_name = 'Membresía de canal'
        verbose_name_plural = 'Membresías de canal'
        unique_together = ['user', 'channel']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.channel.name}"
    
    def get_unread_count(self):
        """Get count of unread messages."""
        return self.channel.messages.filter(
            created_at__gt=self.last_read_at,
            is_deleted=False
        ).exclude(user=self.user).count()
    
    def mark_as_read(self):
        """Mark channel as read up to now."""
        self.last_read_at = timezone.now()
        self.save(update_fields=['last_read_at'])