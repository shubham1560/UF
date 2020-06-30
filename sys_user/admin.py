from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SysUser


class SysUserAdmin(UserAdmin):
    model = SysUser
    list_display = ["id", "email", "username", "is_active", "is_staff", "date_joined", "user_type", "profile"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "profile"),
            },
        ),
    )


# Register your models here.
admin.site.register(SysUser, SysUserAdmin)