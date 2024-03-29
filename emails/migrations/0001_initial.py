# Generated by Django 3.0.7 on 2020-06-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_created_on', models.DateTimeField(auto_now=True)),
                ('sys_updated_on', models.DateTimeField(auto_now_add=True)),
                ('body', models.CharField(max_length=1000)),
                ('body_text', models.CharField(max_length=1000)),
                ('subject', models.CharField(max_length=200)),
                ('priority', models.CharField(choices=[('1', 'LOW'), ('2', 'MEDIUM'), ('3', 'HIGH')], default='1', max_length=1)),
                ('comments', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
    ]
