# Generated by Django 3.0.7 on 2020-07-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_user', '0007_auto_20200709_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysuser',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]
