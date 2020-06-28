from django.db import models
from emails.models import Email
# Create your models here.


EMAIL_TYPES = (
        ('SR', 'Single Recipient'),
        ('MR', 'Multiple Recipient'),
    )

STATUS = (
    ('1', 'Sent'),
    ('0', 'Failed')
)


class SysEmailLog(models.Model):
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    recepient = models.EmailField(blank=True, null=True, max_length=50)
    recepients = models.TextField(blank=True, null=True)
    type = models.CharField(choices=EMAIL_TYPES, default='SR', max_length=2)
    email_body = models.TextField()
    status = models.CharField(choices=STATUS, max_length=1)
    comments = models.TextField()
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Email logs"
