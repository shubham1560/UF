from django.db import models

# Create your models here.
PRIORITY = [
    ('1', 'LOW'),
    ('2', 'MEDIUM'),
    ('3', 'HIGH'),
]


class Email(models.Model):
    sys_created_on = models.DateTimeField(auto_now=True)
    sys_updated_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    footer = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY, default='1')

