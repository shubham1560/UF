# Generated by Django 3.0.7 on 2020-11-18 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqanda', '0004_auto_20201118_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='id',
            field=models.CharField(max_length=32, primary_key=True, serialize=False),
        ),
    ]
