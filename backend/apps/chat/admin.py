from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Channel, Message, ChannelMembership


class MessageInline(admin.TabularInline):
    model = Message
    fields = ['user', 'content', 'file', 'created_at', 'is_deleted']
    readonly_fields = ['created_at']
    extra = 0
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by', 'is_active', 'created_at', 'member_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'created_by']
    inlines = [MessageInline]
    
    def member_count(self, obj):
        return obj.get_member_count()
    member_count.short_description = 'Miembros'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'channel', 'user', 'content_preview', 'has_file', 'created_at', 'is_deleted']
    list_filter = ['channel', 'is_deleted', 'file_type', 'created_at']
    search_fields = ['content', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['created_at', 'edited_at', 'file_preview']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información del mensaje', {
            'fields': ('channel', 'user', 'content')
        }),
        ('Archivo adjunto', {
            'fields': ('file', 'file_preview', 'file_type', 'file_name'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'edited_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: #999;">[Mensaje eliminado]</span>')
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Vista previa'
    
    def has_file(self, obj):
        return bool(obj.file)
    has_file.boolean = True
    has_file.short_description = 'Archivo'
    
    def file_preview(self, obj):
        if not obj.file:
            return "Sin archivo"
        
        if obj.file_type == 'image':
            return mark_safe(f'<img src="{obj.file.url}" style="max-width: 200px; height: auto;" />')
        else:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.file.url,
                obj.file_name or 'Descargar archivo'
            )
    file_preview.short_description = 'Vista previa del archivo'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('channel', 'user')
    
    actions = ['soft_delete_messages']
    
    def soft_delete_messages(self, request, queryset):
        count = 0
        for message in queryset:
            if not message.is_deleted:
                message.soft_delete()
                count += 1
        self.message_user(request, f'{count} mensajes eliminados.')
    soft_delete_messages.short_description = 'Eliminar mensajes (soft delete)'


@admin.register(ChannelMembership)
class ChannelMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel', 'joined_at', 'last_read_at', 'unread_count']
    list_filter = ['channel', 'joined_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'channel__name']
    readonly_fields = ['joined_at']
    
    def unread_count(self, obj):
        return obj.get_unread_count()
    unread_count.short_description = 'Mensajes sin leer'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'channel')