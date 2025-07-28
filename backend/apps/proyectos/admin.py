from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ProjectCategory, Project, ProjectImage, ProjectDocument, ProjectUpdate


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order', 'projects_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Personalización', {
            'fields': ('icon', 'order')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Registro', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Proyectos'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 0
    fields = ['title', 'file', 'description', 'is_public']


class ProjectUpdateInline(admin.StackedInline):
    model = ProjectUpdate
    extra = 0
    fields = ['title', 'content', 'image', 'is_milestone']
    readonly_fields = ['created_by', 'created_at']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'location_display', 'units', 'participants',
        'status_badge', 'is_featured', 'is_active', 'views'
    ]
    list_filter = [
        'category', 'status', 'is_featured', 'is_active',
        'province', 'created_at'
    ]
    search_fields = ['name', 'city', 'province', 'description']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at', 'created_by']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-is_featured', 'order', '-created_at']
    inlines = [ProjectImageInline, ProjectDocumentInline, ProjectUpdateInline]
    autocomplete_fields = ['category', 'partner']
    
    fieldsets = (
        ('Información básica', {
            'fields': (
                'name', 'slug', 'category', 'short_description', 
                'description', 'image'
            ),
            'description': 'La descripción corta se muestra en las tarjetas del listado. Si se deja vacía, se generará automáticamente desde la descripción completa.'
        }),
        ('Ubicación', {
            'fields': (
                'city', 'province', 'address', 'coordinates'
            )
        }),
        ('Características del proyecto', {
            'fields': (
                'units', 'participants', 'status', 'features'
            )
        }),
        ('Fechas', {
            'fields': (
                'start_date', 'estimated_completion'
            )
        }),
        ('Información financiera', {
            'fields': (
                'investment_range', 'financing_type'
            ),
            'classes': ('collapse',)
        }),
        ('Colaboradores', {
            'fields': ('partner',),
            'classes': ('collapse',)
        }),
        ('Enlaces externos', {
            'fields': ('website', 'video_url'),
            'classes': ('collapse',)
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
    
    def location_display(self, obj):
        return obj.get_location()
    location_display.short_description = 'Ubicación'
    
    def status_badge(self, obj):
        colors = {
            'planning': '#6B7280',
            'development': '#3B82F6',
            'construction': '#F59E0B',
            'active': '#10B981',
            'completed': '#8B5CF6',
            'paused': '#D1D5DB'
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; '
            'background-color: {}; color: white; border-radius: 4px; '
            'font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ProjectUpdate) and not instance.created_by:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'created_by')


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'project', 'caption', 'order', 'created_at']
    list_filter = ['project__category', 'created_at']
    search_fields = ['project__name', 'caption']
    ordering = ['project', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Vista previa'


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'file_link', 'is_public', 'created_at']
    list_filter = ['is_public', 'project__category', 'created_at']
    search_fields = ['title', 'project__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Descargar</a>',
                obj.file.url
            )
        return '-'
    file_link.short_description = 'Archivo'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'project', 'is_milestone', 
        'created_by', 'created_at'
    ]
    list_filter = [
        'is_milestone', 'project__category', 
        'created_at', 'project__status'
    ]
    search_fields = ['title', 'content', 'project__name']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'content', 'image')
        }),
        ('Configuración', {
            'fields': ('is_milestone',)
        }),
        ('Información', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('project', 'created_by')