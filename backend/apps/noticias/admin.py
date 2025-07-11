from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published', 'featured', 'views', 'created_at']
    list_filter = ['published', 'featured', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at', 'preview_image']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_editable = ['published', 'featured']
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('Imagen', {
            'fields': ('header_image', 'preview_image'),
            'classes': ('wide',)
        }),
        ('Publicación', {
            'fields': ('author', 'published', 'featured'),
            'classes': ('wide',)
        }),
        ('Estadísticas', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.header_image:
            return mark_safe(f'<img src="{obj.header_image.url}" style="max-width: 300px; height: auto;" />')
        return "Sin imagen"
    preview_image.short_description = 'Vista previa'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


# Configuración del sitio de administración
admin.site.site_header = "Calicanto - Panel de Administración"
admin.site.site_title = "Calicanto Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"