from django.db import models
from django.contrib.auth.models import AbstractUser


class SysUser(AbstractUser):
    profile = models.ImageField(upload_to='pics', null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)

