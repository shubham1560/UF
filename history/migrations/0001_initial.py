# Generated by Django 3.0.7 on 2020-10-30 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SysHistoryLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('table', models.CharField(blank=True, max_length=50, null=True)),
                ('table_sys_id', models.CharField(blank=True, max_length=50, null=True)),
                ('additional_comment', models.CharField(blank=True, max_length=400, null=True)),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
