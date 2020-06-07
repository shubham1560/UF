from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SysUser


class SysUserAdmin(UserAdmin):
    model = SysUser
    list_display = ["email", "username", 'profile', "is_staff"]
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