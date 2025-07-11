from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.models import Count
from .models import Category, Directory, RepositoryFile


class DirectoryInline(admin.TabularInline):
    model = Directory
    fields = ['name', 'is_public', 'created_by']
    readonly_fields = ['created_by']
    extra = 0
    
    def has_add_permission(self, request, obj=None):
        return True


class RepositoryFileInline(admin.TabularInline):
    model = RepositoryFile
    fields = ['name', 'file', 'license', 'is_public', 'is_hidden']
    extra = 0
    
    def has_add_permission(self, request, obj=None):
        return True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active', 'directories_count', 'files_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    inlines = [DirectoryInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def directories_count(self, obj):
        return obj.directories.count()
    directories_count.short_description = 'Directorios'
    
    def files_count(self, obj):
        return obj.files.count()
    files_count.short_description = 'Archivos'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _directories_count=Count('directories', distinct=True),
            _files_count=Count('files', distinct=True)
        )


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'parent', 'is_public', 'created_by', 'created_at', 'files_count']
    list_filter = ['category', 'is_public', 'created_at']
    search_fields = ['name']
    autocomplete_fields = ['parent', 'allowed_users']
    readonly_fields = ['created_by', 'created_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'category', 'parent')
        }),
        ('Permisos', {
            'fields': ('is_public', 'allowed_users'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def files_count(self, obj):
        return obj.files.count()
    files_count.short_description = 'Archivos'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'parent', 'created_by').annotate(
            _files_count=Count('files')
        )


@admin.register(RepositoryFile)
class RepositoryFileAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'directory', 'license_badge', 'size_display', 
        'uploaded_by', 'uploaded_at', 'downloads', 'visibility_status'
    ]
    list_filter = ['category', 'license', 'is_public', 'is_hidden', 'uploaded_at']
    search_fields = ['name', 'description']
    autocomplete_fields = ['allowed_users']
    readonly_fields = [
        'size', 'mime_type', 'uploaded_by', 'uploaded_at', 'modified_at', 
        'downloads', 'file_preview', 'file_info'
    ]
    date_hierarchy = 'uploaded_at'
    
    fieldsets = (
        ('Información del archivo', {
            'fields': ('name', 'file', 'category', 'directory', 'description')
        }),
        ('Licencia', {
            'fields': ('license',)
        }),
        ('Permisos', {
            'fields': ('is_public', 'is_hidden', 'allowed_users'),
        }),
        ('Información técnica', {
            'fields': ('file_preview', 'file_info', 'mime_type', 'downloads'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('uploaded_by', 'uploaded_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_public', 'make_private', 'toggle_hidden']
    
    def license_badge(self, obj):
        colors = {
            'CC0': 'green',
            'CC-BY': 'blue',
            'CC-BY-SA': 'blue',
            'CC-BY-NC': 'orange',
            'CC-BY-NC-SA': 'orange',
            'Apache-2.0': 'purple',
            'MIT': 'purple',
            'GPL-3.0': 'red',
            'Copyleft': 'green',
            'Copyright': 'gray',
            'Other': 'gray',
        }
        color = colors.get(obj.license, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_license_display()
        )
    license_badge.short_description = 'Licencia'
    
    def size_display(self, obj):
        if not obj.size:
            return "N/A"
        size = obj.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    size_display.short_description = 'Tamaño'
    
    def visibility_status(self, obj):
        if not obj.pk:  # Si el objeto es nuevo
            return "N/A"
        
        icons = []
        if obj.is_hidden:
            icons.append('<span title="Oculto">🚫</span>')
        if not obj.is_public:
            icons.append('<span title="Privado">🔒</span>')
        if obj.allowed_users.exists():
            icons.append('<span title="Usuarios específicos">👥</span>')
        return format_html(' '.join(icons)) if icons else '✅'
    visibility_status.short_description = 'Estado'
    
    def file_preview(self, obj):
        if not obj.file:
            return "Sin archivo"
        
        ext = obj.get_extension().lower()
        
        # Preview for images
        if ext in ['jpg', 'jpeg', 'png', 'gif']:
            return mark_safe(
                f'<img src="{obj.file.url}" style="max-width: 300px; max-height: 200px;" />'
            )
        
        # Link for other files
        return format_html(
            '<a href="{}" target="_blank" class="button">Ver archivo</a>',
            obj.file.url
        )
    file_preview.short_description = 'Vista previa'
    
    def file_info(self, obj):
        if not obj.file:
            return "No hay archivo cargado aún"
        
        info = f"<strong>Nombre original:</strong> {obj.file.name}<br>"
        info += f"<strong>Tipo MIME:</strong> {obj.mime_type or 'N/A'}<br>"
        info += f"<strong>Extensión:</strong> {obj.get_extension() if obj.file else 'N/A'}<br>"
        info += f"<strong>Tamaño:</strong> {self.size_display(obj)}<br>"
        info += f"<strong>Icono:</strong> {obj.get_icon() if obj.file else 'N/A'}<br>"
        info += f"<strong>Vista previa disponible:</strong> {'Sí' if obj.file and obj.can_preview() else 'No'}"
        return mark_safe(info)
    file_info.short_description = 'Información del archivo'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.uploaded_by = request.user
            # Si no se especificó un nombre, usar el nombre del archivo
            if obj.file and not form.data.get('name'):
                obj.name = obj.file.name.split('/')[-1]
        super().save_model(request, obj, form, change)
    
    def make_public(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f'{updated} archivos marcados como públicos.')
    make_public.short_description = 'Hacer públicos los archivos seleccionados'
    
    def make_private(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f'{updated} archivos marcados como privados.')
    make_private.short_description = 'Hacer privados los archivos seleccionados'
    
    def toggle_hidden(self, request, queryset):
        for obj in queryset:
            obj.is_hidden = not obj.is_hidden
            obj.save()
        self.message_user(request, f'{queryset.count()} archivos actualizados.')
    toggle_hidden.short_description = 'Alternar visibilidad de archivos'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'directory', 'uploaded_by')