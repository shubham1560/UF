# Generated by Django 3.0.7 on 2020-11-09 16:58

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
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField()),
                ('active', models.BooleanField(default=True)),
                ('answer', models.TextField(blank=True, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('votes', models.IntegerField(blank=True, default=0, null=True)),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('table_id', models.CharField(blank=True, max_length=10, null=True)),
                ('table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('up_vote', models.BooleanField(blank=True, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('answer_count', models.IntegerField(blank=True, default=0, null=True)),
                ('question', models.CharField(blank=True, max_length=120, null=True)),
                ('question_details', models.TextField(blank=True, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('views', models.IntegerField(default=0)),
                ('votes', models.IntegerField(default=0)),
                ('accepted_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_accepted_for_question', to='sqanda.Answer')),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManyToManyTaggedObjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.CharField(blank=True, max_length=10, null=True)),
                ('table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m2m_tag_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m2m_tag_updated_by', to=settings.AUTH_USER_MODEL)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sqanda.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('table_id', models.CharField(blank=True, max_length=10, null=True)),
                ('table_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('sys_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_created_by', to=settings.AUTH_USER_MODEL)),
                ('sys_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sqanda.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='sys_created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='sys_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]