# Generated by Django 3.0.7 on 2020-06-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sys_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysuser',
            name='user_type',
            field=models.CharField(choices=[('GU', 'GOOGLE'), ('RU', 'ROOT')], default='RU', max_length=2),
        ),
    ]