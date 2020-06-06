from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SysUser


class SysUserAdmin(UserAdmin):
    model = SysUser


# Register your models here.
admin.site.register(SysUser, SysUserAdmin)