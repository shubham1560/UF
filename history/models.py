from django.db import models
from sys_user.models import SysUser
# Create your models here.


class SysHistoryLine(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)
    sys_created_by = models.ForeignKey(SysUser, related_name="history_created_by",
                                       on_delete=models.CASCADE, blank=True, null=True)
    sys_updated_by = models.ForeignKey(SysUser, related_name="history_updated_by",
                                       on_delete=models.CASCADE, blank=True, null=True)
    table = models.CharField(max_length=50, blank=True, null=True)
    table_sys_id = models.CharField(max_length=50, blank=True, null=True)
    additional_comment = models.CharField(max_length=400, blank=True, null=True)
