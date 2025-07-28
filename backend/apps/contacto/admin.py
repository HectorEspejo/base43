# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactMessage model
    """
    list_display = [
        'full_name', 'email', 'subject_badge', 'status_badge', 
        'created_at_formatted', 'phone', 'is_registered_user'
    ]
    list_filter = [
        'status', 'subject', 'created_at',
        ('user', admin.EmptyFieldListFilter),
    ]
    search_fields = ['name', 'surname', 'email', 'message', 'phone']
    readonly_fields = [
        'name', 'surname', 'email', 'phone', 'subject', 'message',
        'created_at', 'updated_at', 'ip_address', 'user_agent', 'user'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información de contacto', {
            'fields': ('name', 'surname', 'email', 'phone', 'user')
        }),
        ('Mensaje', {
            'fields': ('subject', 'message')
        }),
        ('Estado y notas', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Nombre completo'
    
    def subject_badge(self, obj):
        colors = {
            'informacion': 'blue',
            'proyecto': 'green',
            'colaboracion': 'purple',
            'tecnico': 'orange',
            'otro': 'gray',
        }
        color = colors.get(obj.subject, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_subject_display()
        )
    subject_badge.short_description = 'Asunto'
    
    def status_badge(self, obj):
        colors = {
            'new': '#dc3545',      # red
            'read': '#ffc107',     # yellow
            'answered': '#28a745', # green
            'archived': '#6c757d', # gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def created_at_formatted(self, obj):
        """Format creation date in Spanish format"""
        local_time = timezone.localtime(obj.created_at)
        return local_time.strftime('%d/%m/%Y %H:%M')
    created_at_formatted.short_description = 'Fecha de envío'
    
    def is_registered_user(self, obj):
        if obj.user:
            return format_html(
                '<span style="color: green;">✓</span>'
            )
        return format_html(
            '<span style="color: red;">✗</span>'
        )
    is_registered_user.short_description = 'Usuario registrado'
    
    def has_add_permission(self, request):
        # Prevent adding messages from admin
        return False
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Mark message as read when opened
        if object_id:
            message = self.get_object(request, object_id)
            if message and message.status == 'new':
                message.mark_as_read()
        
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    actions = ['mark_as_answered', 'mark_as_archived']
    
    def mark_as_answered(self, request, queryset):
        updated = queryset.update(status='answered')
        self.message_user(
            request,
            f'{updated} mensaje(s) marcado(s) como respondido(s).'
        )
    mark_as_answered.short_description = 'Marcar como respondido'
    
    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(
            request,
            f'{updated} mensaje(s) archivado(s).'
        )
    mark_as_archived.short_description = 'Archivar mensajes'