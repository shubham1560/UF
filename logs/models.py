from django.db import models
from emails.models import Email
# Create your models here.
from sys_user.models import SysUser

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
    recipient = models.EmailField(blank=True, null=True, max_length=50)
    recipients = models.TextField(blank=True, null=True)
    sent_from = models.EmailField(max_length=100, blank=True, null=True)
    type = models.CharField(choices=EMAIL_TYPES, default='SR', max_length=2, blank=True)
    email_body = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, max_length=1, blank=True)
    mail_sent_number = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Email logs"


class RequestLog(models.Model):
    viewset = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    request_body = models.TextField(null=True)
    request_header = models.TextField(null=True)
    response_data = models.TextField()
    status = models.CharField(max_length=50)
    time_elapsed = models.CharField(max_length=40, blank=True, null=True)
    # time_elapsed = models.DecimalField(max_digits=5, decimal_places=4)
    sys_created_on = models.DateTimeField(auto_now_add=True)
    sys_created_by = models.ForeignKey(SysUser, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Request Logs"


class RandomLog(models.Model):
    sys_created_on = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=4000)
    source = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Random Logs"
