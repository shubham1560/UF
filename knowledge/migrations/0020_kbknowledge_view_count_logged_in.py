# Generated by Django 3.0.7 on 2020-07-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0019_auto_20200713_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbknowledge',
            name='view_count_logged_in',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]