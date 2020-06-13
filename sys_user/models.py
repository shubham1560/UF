from django.db import models
from django.contrib.auth.models import AbstractUser


class SysUser(AbstractUser):

    USER_TPYE = [
        ('GU', 'GOOGLE'),
        ('RU', 'ROOT'),
    ]

    profile = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    user_type = models.CharField(max_length=2, choices=USER_TPYE, default='RU')

