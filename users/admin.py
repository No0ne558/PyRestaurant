from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('number_id', 'is_staff', 'is_superuser')
    search_fields = ('number_id',)
    ordering = ('number_id',)

    # Only show number_id, remove username/password fields
    fieldsets = (
        (None, {'fields': ('number_id', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(User, CustomUserAdmin)
