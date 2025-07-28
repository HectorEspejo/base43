# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactMessage(models.Model):
    """
    Model to store contact form messages
    """
    SUBJECT_CHOICES = [
        ('informacion', 'Información general'),
        ('proyecto', 'Sobre un proyecto'),
        ('colaboracion', 'Propuesta de colaboración'),
        ('tecnico', 'Soporte técnico'),
        ('otro', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('read', 'Leído'),
        ('answered', 'Respondido'),
        ('archived', 'Archivado'),
    ]
    
    # Contact information
    name = models.CharField(max_length=100, verbose_name='Nombre')
    surname = models.CharField(max_length=100, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    
    # Message details
    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        verbose_name='Asunto'
    )
    message = models.TextField(verbose_name='Mensaje')
    
    # Metadata
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de envío')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    # Optional fields for tracking
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, null=True, verbose_name='User Agent')
    
    # If the sender is a registered user
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_messages',
        verbose_name='Usuario registrado'
    )
    
    # Admin notes
    admin_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Notas del administrador',
        help_text='Notas internas sobre este mensaje'
    )
    
    class Meta:
        db_table = 'contact_messages'
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} {self.surname} - {self.get_subject_display()} ({self.created_at.strftime('%d/%m/%Y')})"
    
    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
    
    @property
    def is_new(self):
        return self.status == 'new'
    
    def mark_as_read(self):
        if self.status == 'new':
            self.status = 'read'
            self.save()