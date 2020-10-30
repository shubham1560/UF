# Generated by Django 3.0.7 on 2020-10-29 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attachments', '0003_attachedimage_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachedimage',
            name='sys_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachedimage',
            name='table',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='attachedimage',
            name='table_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]