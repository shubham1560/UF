from django.contrib import admin
from .models import SysEmailLog, RequestLog, RandomLog


# Register your models here.
class SysEmailLogAdmin(admin.ModelAdmin):
    model = SysEmailLog
    list_display = ['id', 'email', 'recipient', 'recipients', 'email_body', 'comments', 'status', 'sys_created_on']


class RequestLogAdmin(admin.ModelAdmin):
    model = RequestLog
    list_display = ['id', 'viewset', 'method', 'sys_created_by',
                    'request_body', 'response_data', 'status',
                    'time_elapsed', 'sys_created_on']
    empty_value_display = '-empty-'
    list_filter = ('status', 'method', 'viewset', 'sys_created_on')
    search_fields = ['viewset']


class RandomLogsAdmin(admin.ModelAdmin):
    model = RandomLog
    list_display = ['id', 'message', 'source', 'sys_created_on']
    list_filter = ('source', )
    search_fields = ['message']


admin.site.register(SysEmailLog, SysEmailLogAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
admin.site.register(RandomLog, RandomLogsAdmin)