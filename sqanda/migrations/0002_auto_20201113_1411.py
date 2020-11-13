# Generated by Django 3.0.7 on 2020-11-13 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0049_kbknowledge_article_url'),
        ('sqanda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='kb_base',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='knowledge.KbKnowledgeBase'),
        ),
        migrations.AddField(
            model_name='question',
            name='kb_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='knowledge.KbCategory'),
        ),
        migrations.AddField(
            model_name='question',
            name='kb_knowledge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='knowledge.KbKnowledge'),
        ),
    ]
