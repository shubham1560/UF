# Generated by Django 3.0.7 on 2020-07-23 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0024_auto_20200722_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbcategory',
            name='label',
            field=models.CharField(max_length=100),
        ),
    ]
