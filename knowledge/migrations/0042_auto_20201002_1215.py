# Generated by Django 3.0.7 on 2020-10-02 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0041_auto_20201001_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbcategory',
            name='parent_kb_base',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_categories', to='knowledge.KbKnowledgeBase'),
        ),
    ]
