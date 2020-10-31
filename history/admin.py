from .models import SysHistoryLine
from django.contrib import admin


class HistoryAdmin(admin.ModelAdmin):
    model = SysHistoryLine
    list_display = ['id', 'table', 'table_sys_id', 'additional_comment', 'sys_created_by', 'sys_created_on']
    list_filter = ('table', )
    search_fields = ['table', 'table_sys_id']

    class Meta:
        ordering = ['sys_updated_on']


admin.site.register(SysHistoryLine, HistoryAdmin)
