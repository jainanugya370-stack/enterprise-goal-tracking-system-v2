from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department


class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (

        (
            'Custom Fields',
            {
                'fields': (
                    'role',
                    'department',
                    'manager',
                )
            }
        ),

    )

    add_fieldsets = UserAdmin.add_fieldsets + (

        (
            'Custom Fields',
            {
                'fields': (
                    'role',
                    'department',
                    'manager',
                )
            }
        ),

    )


admin.site.register(
    User,
    CustomUserAdmin
)

admin.site.register(
    Department
)