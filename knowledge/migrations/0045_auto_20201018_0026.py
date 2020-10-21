# Generated by Django 3.0.7 on 2020-10-17 18:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('knowledge', '0044_auto_20201005_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbuse',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='kbuse',
            unique_together={('article', 'user', 'course')},
        ),
    ]