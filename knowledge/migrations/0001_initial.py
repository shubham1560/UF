# Generated by Django 3.0.7 on 2020-06-18 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KbCategory',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('sys_created_on', models.DateTimeField(auto_now=True)),
                ('sys_updated_on', models.DateTimeField(auto_now_add=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbCategory')),
            ],
        ),
        migrations.CreateModel(
            name='KbKnowledgeBase',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='KbKnowledge',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('article_type', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=2000)),
                ('disable_commenting', models.BooleanField(default=False)),
                ('disable_suggesting', models.BooleanField(default=False)),
                ('flagged', models.BooleanField(default=False)),
                ('number', models.CharField(max_length=12)),
                ('published_on', models.DateTimeField()),
                ('rating', models.FloatField()),
                ('title', models.CharField(max_length=50)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('view_count', models.IntegerField(default=0)),
                ('article_body', models.TextField()),
                ('topic', models.CharField(max_length=50)),
                ('workflow', models.CharField(choices=[('draft', 'Draft'), ('review', 'Review'), ('published', 'Published'), ('retired', 'Retired'), ('outdated', 'Outdated')], max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbCategory')),
                ('knowledge_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbKnowledgeBase')),
                ('parent_article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='knowledge.KbKnowledge')),
            ],
        ),
        migrations.AddField(
            model_name='kbcategory',
            name='parent_kb_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbKnowledgeBase'),
        ),
    ]
