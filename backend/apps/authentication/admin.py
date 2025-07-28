from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.
    """
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'user_type', 'is_verified', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_verified', 'user_type', 'is_active', 'is_staff',
        'created_at'
    ]
    list_editable = ['is_verified', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'organization']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('user_type', 'phone', 'organization', 'bio', 'avatar', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'phone', 'organization')
        }),
    )
    
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        """Verificar usuarios seleccionados"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} usuario(s) verificado(s) exitosamente.')
    verify_users.short_description = 'Verificar usuarios seleccionados'
    
    def unverify_users(self, request, queryset):
        """Quitar verificación a usuarios seleccionados"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'Se quitó la verificación a {updated} usuario(s).')
    unverify_users.short_description = 'Quitar verificación a usuarios seleccionados'


admin.site.register(User, UserAdmin)