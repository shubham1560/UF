# Generated by Django 3.0.7 on 2020-07-05 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('knowledge', '0009_auto_20200701_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys_created_on', models.DateTimeField(auto_now_add=True)),
                ('sys_updated_on', models.DateTimeField(auto_now=True)),
                ('image_caption', models.CharField(blank=True, max_length=100, null=True)),
                ('real_image', models.ImageField(upload_to='articleimages/real_image/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='articleimages/thumbnail/')),
                ('compressed', models.ImageField(blank=True, null=True, upload_to='articleimages/compressed/')),
                ('article', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.KbKnowledge')),
            ],
        ),
    ]