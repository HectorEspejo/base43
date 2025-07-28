from django.contrib import admin
from django.utils.html import format_html
from .models import Resource, ResourceCategory, ResourceImage, ResourceDocument


class ResourceImageInline(admin.TabularInline):
    """Inline para gestionar imágenes de recursos"""
    model = ResourceImage
    extra = 1
    fields = ['image', 'caption', 'is_main']


class ResourceDocumentInline(admin.TabularInline):
    """Inline para gestionar documentos de recursos"""
    model = ResourceDocument
    extra = 1
    fields = ['title', 'file', 'description']


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    """Administración de categorías de recursos"""
    list_display = ['name', 'description', 'resource_count', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def resource_count(self, obj):
        """Muestra el número de recursos en esta categoría"""
        count = obj.resource_set.count()
        return format_html('<b>{}</b> recursos', count)
    resource_count.short_description = 'Recursos'


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Administración de recursos"""
    list_display = [
        'name', 'type', 'category', 'city', 
        'is_active', 'is_featured', 'has_coordinates', 'created_at'
    ]
    list_filter = [
        'type', 'city', 'category', 'is_active', 'is_featured',
        ('created_at', admin.DateFieldListFilter)
    ]
    search_fields = ['name', 'description', 'address', 'services']
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'full_address']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'type', 'category', 'description')
        }),
        ('Ubicación', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude', 'full_address')
        }),
        ('Contacto', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Información Adicional', {
            'fields': ('schedule', 'services', 'requirements'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Metadatos', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ResourceImageInline, ResourceDocumentInline]
    
    def has_coordinates(self, obj):
        """Indica si el recurso tiene coordenadas GPS"""
        if obj.latitude and obj.longitude:
            return format_html(
                '<span style="color: green;">✓</span> {}, {}',
                obj.latitude, obj.longitude
            )
        return format_html('<span style="color: red;">✗</span> Sin coordenadas')
    has_coordinates.short_description = 'Coordenadas'
    
    def save_model(self, request, obj, form, change):
        """Asigna el usuario que crea el recurso"""
        if not change:  # Si es nuevo
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimiza las consultas incluyendo relaciones"""
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'created_by')
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(ResourceImage)
class ResourceImageAdmin(admin.ModelAdmin):
    """Administración de imágenes de recursos"""
    list_display = ['resource', 'caption', 'is_main', 'image_preview', 'created_at']
    list_filter = ['is_main', 'resource__category', 'created_at']
    search_fields = ['resource__name', 'caption']
    
    def image_preview(self, obj):
        """Muestra una vista previa de la imagen"""
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; width: auto;" />',
                obj.image.url
            )
        return "Sin imagen"
    image_preview.short_description = 'Vista previa'


@admin.register(ResourceDocument)
class ResourceDocumentAdmin(admin.ModelAdmin):
    """Administración de documentos de recursos"""
    list_display = ['title', 'resource', 'file_link', 'created_at']
    list_filter = ['resource__category', 'created_at']
    search_fields = ['title', 'resource__name', 'description']
    
    def file_link(self, obj):
        """Muestra un enlace al archivo"""
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Ver documento</a>',
                obj.file.url
            )
        return "Sin archivo"
    file_link.short_description = 'Archivo'