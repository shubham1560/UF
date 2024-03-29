# Generated by Django 3.0.7 on 2020-07-22 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0022_kbuse_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='kbcategory',
            name='compressed_image',
            field=models.ImageField(blank=True, null=True, upload_to='knowledge_base/compressed_images/'),
        ),
        migrations.AddField(
            model_name='kbcategory',
            name='real_image',
            field=models.ImageField(blank=True, null=True, upload_to='knowledge_base/real_images/'),
        ),
        migrations.AddField(
            model_name='kbknowledgebase',
            name='compressed_image',
            field=models.ImageField(blank=True, null=True, upload_to='knowledge_base/compressed_images/'),
        ),
        migrations.AddField(
            model_name='kbknowledgebase',
            name='real_image',
            field=models.ImageField(blank=True, null=True, upload_to='knowledge_base/real_images/'),
        ),
    ]
