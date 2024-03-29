# Generated by Django 3.0.7 on 2020-07-07 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('knowledge', '0013_auto_20200706_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkUserArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbKnowledge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bookmarks User Articles',
                'unique_together': {('article', 'user')},
            },
        ),
    ]
