from django.contrib import admin
from .models import SysEmailLog


# Register your models here.
class SysEmailLogAdmin(admin.ModelAdmin):
    model = SysEmailLog
    list_display = ['id', 'email', 'recipient', 'recipients', 'email_body', 'comments', 'status']


admin.site.register(SysEmailLog, SysEmailLogAdmin)
