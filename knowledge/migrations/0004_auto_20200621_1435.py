# Generated by Django 3.0.7 on 2020-06-21 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('knowledge', '0003_kbuse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kbcategory',
            options={'verbose_name_plural': 'Knowledge Categories'},
        ),
        migrations.AlterModelOptions(
            name='kbfeedback',
            options={'verbose_name_plural': 'Knowledge Feedbacks'},
        ),
        migrations.AlterModelOptions(
            name='kbknowledge',
            options={'verbose_name_plural': 'Knowledge Articles'},
        ),
        migrations.AlterModelOptions(
            name='kbknowledgebase',
            options={'verbose_name_plural': 'Knowledge Bases'},
        ),
        migrations.AlterModelOptions(
            name='kbuse',
            options={'verbose_name_plural': 'Knowledge Uses'},
        ),
        migrations.AlterField(
            model_name='kbknowledge',
            name='number',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.CreateModel(
            name='m2m_knowledge_feedback_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbFeedback')),
                ('commented_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Knowledge Feedback Likes',
            },
        ),
    ]
