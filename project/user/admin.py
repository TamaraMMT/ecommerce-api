"""
Admin customization
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from user.models import User


class UserAdmin(BaseUserAdmin):
    """Show in admin page"""
    list_display = (
        'id',
        'firstname',
        'lastname',
        'email',
        'is_staff',
        'is_active'
    )
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('firstname', 'lastname')}),
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
                'firstname',
                'lastname',
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
