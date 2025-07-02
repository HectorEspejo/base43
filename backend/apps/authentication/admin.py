from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
        'user_type', 'is_verified', 'is_active', 'is_staff',
        'created_at'
    ]
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


admin.site.register(User, UserAdmin)