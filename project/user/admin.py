"""
Admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User, UserProfile


class UserAdmin(BaseUserAdmin):
    """Show in admin page"""
    list_display = (
        'id',
        'email',
        'is_staff',
        'is_active'
    )
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
    readonly_fields = ['last_login']


admin.site.register(User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
    )
    fieldsets = (
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'user')}),
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'last_name',
            ),
        }),
    )

    readonly_fields = ['user']


admin.site.register(UserProfile, UserProfileAdmin)
