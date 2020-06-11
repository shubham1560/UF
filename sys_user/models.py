from django.db import models
from django.contrib.auth.models import AbstractUser


class SysUser(AbstractUser):
    profile = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)

