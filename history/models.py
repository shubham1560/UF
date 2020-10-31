from django.db import models
from sys_user.models import SysUser
from decouple import config


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

    def get_created_by(self):
        if self.sys_created_by.profile:
            pic = str(config('S3URL')) + str(self.sys_created_by.profile)
        elif self.sys_created_by.profile_pic:
            pic = self.sys_created_by.profile_pic
        else:
            pic = ''
        return {
            "first_name": self.sys_created_by.first_name,
            "last_name": self.sys_created_by.last_name,
            'pic': pic
            # "email": self.sys_created_by.email
        }
