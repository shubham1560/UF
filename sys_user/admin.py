from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SysUser, SubscriptionList


class SysUserAdmin(UserAdmin):
    model = SysUser
    list_display = ["id_name",
                    "email",
                    "username",
                    "is_active",
                    "is_staff",
                    'facebook_id',
                    "user_type",
                    "public",
                    "date_joined",
                    "password_needs_reset"
                    ]
    # sortable_by = ('-date_joined', )
    ordering = ('-date_joined',)
    # list_editable = ('is_active',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "id_name", 'password_needs_reset'),
            },
        ),
    )


class SubscriptionListAdmin(admin.ModelAdmin):
    model = SubscriptionList
    list_display = ['email', 'active', 'sys_created_on']


# Register your models here.
admin.site.register(SysUser, SysUserAdmin)
admin.site.register(SubscriptionList, SubscriptionListAdmin)