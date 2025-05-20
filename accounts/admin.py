from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone', 'full_name', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('phone', 'full_name', 'email')
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal Info'), {'fields': ('full_name', 'email', 'avatar')}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Extra Info'), {'fields': ('ip_address',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'is_active', 'is_staff')}
        ),
    )
