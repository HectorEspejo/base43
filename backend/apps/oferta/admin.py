from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ServiceCategory, Service, ServiceInquiry


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'icon', 'order', 'services_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Personalización', {
            'fields': ('icon', 'color', 'order')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Registro', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 60px; height: 20px; '
            'background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></span>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = 'Servicios'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _services_count=Count('services')
        )
        return queryset


class ServiceImageInline(admin.TabularInline):
    model = Service
    fields = ['image']
    extra = 1
    max_num = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price_type', 'price_display', 
        'provider_name', 'is_featured', 'is_active', 'views'
    ]
    list_filter = [
        'category', 'price_type', 'is_featured', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'description', 'provider_name', 'provider_email']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at', 'created_by']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-is_featured', 'order', 'name']
    
    fieldsets = (
        ('Información básica', {
            'fields': (
                'name', 'slug', 'category', 'description', 
                'short_description', 'image'
            )
        }),
        ('Detalles del servicio', {
            'fields': (
                'features', 'requirements', 'duration'
            ),
            'classes': ('wide',)
        }),
        ('Precio', {
            'fields': (
                'price_type', 'price_min', 'price_max', 'price_note'
            )
        }),
        ('Proveedor', {
            'fields': (
                'provider_name', 'provider_email', 
                'provider_phone', 'provider_website'
            )
        }),
        ('Configuración', {
            'fields': (
                'is_featured', 'is_active', 'order'
            )
        }),
        ('Estadísticas', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
        ('Registro', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return obj.get_price_display()
    price_display.short_description = 'Precio'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'created_by')


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'service', 'created_at', 
        'is_read', 'is_answered', 'answered_by'
    ]
    list_filter = [
        'is_read', 'is_answered', 'created_at', 
        'service__category'
    ]
    search_fields = ['name', 'email', 'message', 'service__name']
    readonly_fields = [
        'service', 'name', 'email', 'phone', 'message',
        'created_at', 'answered_at', 'answered_by'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información de contacto', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Consulta', {
            'fields': ('service', 'message')
        }),
        ('Estado', {
            'fields': ('is_read', 'is_answered', 'notes')
        }),
        ('Registro', {
            'fields': ('created_at', 'answered_at', 'answered_by'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_answered']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(
            request,
            f'{updated} consultas marcadas como leídas.'
        )
    mark_as_read.short_description = 'Marcar como leídas'
    
    def mark_as_answered(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            is_answered=True,
            answered_at=timezone.now(),
            answered_by=request.user
        )
        self.message_user(
            request,
            f'{updated} consultas marcadas como respondidas.'
        )
    mark_as_answered.short_description = 'Marcar como respondidas'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('service', 'service__category', 'answered_by')
    
    def has_add_permission(self, request):
        # No permitir crear consultas desde el admin
        return False
    
    def has_change_permission(self, request, obj=None):
        # Solo permitir editar para marcar como leída/respondida
        return request.user.has_perm('oferta.change_serviceinquiry')