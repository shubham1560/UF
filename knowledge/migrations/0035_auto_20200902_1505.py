# Generated by Django 3.0.7 on 2020-09-02 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0034_auto_20200727_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kbcategory',
            name='parent_kb_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_categories', to='knowledge.KbKnowledgeBase'),
        ),
    ]
