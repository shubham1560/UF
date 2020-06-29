from django.contrib import admin
from .models import SysEmailLog, RequestLog, RandomLogs


# Register your models here.
class SysEmailLogAdmin(admin.ModelAdmin):
    model = SysEmailLog
    list_display = ['id', 'email', 'recipient', 'recipients', 'email_body', 'comments', 'status']


class RequestLogAdmin(admin.ModelAdmin):
    model = RequestLog
    list_display = ['id', 'viewset', 'method', 'request_body', 'response_data', 'status', 'time_elapsed']
    empty_value_display = '-empty-'
    list_filter = ('status', 'method', 'viewset', 'sys_created_on')
    search_fields = ['viewset']


class RandomLogsAdmin(admin.ModelAdmin):
    model = RandomLogs
    list_display = ['id', 'message', 'source']
    list_filter = ('source', )
    search_fields = ['message']


admin.site.register(SysEmailLog, SysEmailLogAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(RandomLogs, RandomLogsAdmin)