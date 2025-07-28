from django.contrib import admin
from django.utils.html import format_html
from .models import PartnerCategory, Partner, PartnerTestimonial, PartnerProject


class PartnerTestimonialInline(admin.TabularInline):
    """Inline para testimonios de partners"""
    model = PartnerTestimonial
    extra = 0
    fields = ['author', 'role', 'content', 'is_active']


class PartnerProjectInline(admin.TabularInline):
    """Inline para proyectos de partners"""
    model = PartnerProject
    extra = 0
    fields = ['project', 'role', 'start_date', 'end_date', 'is_active']
    autocomplete_fields = ['project']


@admin.register(PartnerCategory)
class PartnerCategoryAdmin(admin.ModelAdmin):
    """Admin para categorías de partners"""
    list_display = ['name', 'slug', 'order', 'partners_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def partners_count(self, obj):
        """Cuenta de partners en la categoría"""
        return obj.partners.filter(is_active=True).count()
    partners_count.short_description = 'Nº Partners'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    """Admin para partners"""
    list_display = [
        'name', 'partner_type', 'category', 'city', 'province',
        'is_featured', 'is_active', 'order', 'logo_preview'
    ]
    list_filter = [
        'partner_type', 'category', 'is_featured', 'is_active',
        'province', 'created_at'
    ]
    search_fields = ['name', 'description', 'mission', 'city', 'province']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    readonly_fields = ['created_at', 'updated_at', 'logo_preview_large']
    inlines = [PartnerTestimonialInline, PartnerProjectInline]
    ordering = ['-is_featured', 'order', 'name']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'name', 'slug', 'partner_type', 'category',
                'is_featured', 'is_active', 'order'
            )
        }),
        ('Descripción', {
            'fields': ('description', 'mission')
        }),
        ('Contacto', {
            'fields': (
                'contact_person', 'email', 'phone', 'website'
            )
        }),
        ('Ubicación', {
            'fields': (
                'address', 'city', 'province', 'postal_code'
            )
        }),
        ('Redes Sociales', {
            'fields': (
                'linkedin', 'twitter', 'facebook', 'instagram'
            ),
            'classes': ('collapse',)
        }),
        ('Colaboración', {
            'fields': (
                'collaboration_areas', 'collaboration_start'
            )
        }),
        ('Imágenes', {
            'fields': (
                'logo', 'logo_preview_large', 'featured_image'
            )
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def logo_preview(self, obj):
        """Vista previa del logo en la lista"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="height: 40px; width: auto;"/>',
                obj.logo.url
            )
        return '-'
    logo_preview.short_description = 'Logo'
    
    def logo_preview_large(self, obj):
        """Vista previa grande del logo"""
        if obj.logo:
            return format_html(
                '<img src="{}" style="height: 150px; width: auto;"/>',
                obj.logo.url
            )
        return 'No hay logo'
    logo_preview_large.short_description = 'Vista previa del logo'
    
    def save_model(self, request, obj, form, change):
        """Guardar el modelo"""
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/partners.css',)
        }


@admin.register(PartnerTestimonial)
class PartnerTestimonialAdmin(admin.ModelAdmin):
    """Admin para testimonios"""
    list_display = ['partner', 'author', 'role', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'partner']
    search_fields = ['author', 'role', 'content', 'partner__name']
    autocomplete_fields = ['partner']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('partner', 'author', 'role', 'content', 'is_active')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PartnerProject)
class PartnerProjectAdmin(admin.ModelAdmin):
    """Admin para colaboraciones en proyectos"""
    list_display = [
        'partner', 'project', 'role', 'start_date', 
        'end_date', 'is_active'
    ]
    list_filter = ['is_active', 'start_date', 'partner', 'project__category']
    search_fields = [
        'partner__name', 'project__name', 'role', 'description'
    ]
    autocomplete_fields = ['partner', 'project']
    readonly_fields = ['created_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        (None, {
            'fields': (
                'partner', 'project', 'role', 'description'
            )
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date')
        }),
        ('Estado', {
            'fields': ('is_active', 'created_at')
        })
    )