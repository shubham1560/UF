# Generated by Django 3.0.7 on 2020-09-03 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0037_knowledgesection_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbknowledge',
            name='category',
            field=models.ForeignKey(blank=True, default='random', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_category', to='knowledge.KbCategory'),
        ),
    ]
