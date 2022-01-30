from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from api_server.apps.custom_accounts.models import CustomUser, GenderMaster


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser"""
    model = CustomUser
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('user_id', 'email', 'is_staff', 'is_superuser', 'is_active', 'groups',)
    fieldsets = (
        (None, {'fields': ('uuid', 'user_id', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'birthday', 'gender')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('uuid', 'user_id', 'email',)
    ordering = ('user_id', 'email',)

    readonly_fields = ('uuid', 'user_id',)


admin.site.register(CustomUser, CustomUserAdmin)

models = [
    GenderMaster,
]
admin.site.register(models)
