# Generated by Django 3.0.7 on 2020-07-12 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0015_auto_20200707_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbknowledge',
            name='category',
            field=models.ForeignKey(default='random', on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbCategory'),
        ),
    ]
