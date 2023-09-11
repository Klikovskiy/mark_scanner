from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active', 'price_multiply')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Доп. информация', {'fields': ('price_multiply',)}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Данные входа', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_active', 'is_staff',
                'is_superuser'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(CustomUser, CustomUserAdmin)
