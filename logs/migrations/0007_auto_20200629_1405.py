# Generated by Django 3.0.7 on 2020-06-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_requestlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestlog',
            old_name='function',
            new_name='viewset',
        ),
        migrations.AddField(
            model_name='requestlog',
            name='method',
            field=models.CharField(default='ola', max_length=10),
            preserve_default=False,
        ),
    ]
