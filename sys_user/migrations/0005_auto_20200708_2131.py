# Generated by Django 3.0.7 on 2020-07-08 21:31

from django.db import migrations, models
import sys_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_user', '0004_auto_20200708_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysuser',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to=sys_user.models.upload_path_compress),
        ),
    ]
