from django.contrib import admin
from .models import SysEmailLog, RequestLog


# Register your models here.
class SysEmailLogAdmin(admin.ModelAdmin):
    model = SysEmailLog
    list_display = ['id', 'email', 'recipient', 'recipients', 'email_body', 'comments', 'status']


class RequestLogAdmin(admin.ModelAdmin):
    model = RequestLog
    list_display = ['id', 'method', 'request_body', 'response_data', 'status', 'time_elapsed']


admin.site.register(SysEmailLog, SysEmailLogAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
