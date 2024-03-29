# Generated by Django 3.0.7 on 2020-06-29 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0007_auto_20200629_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysemaillog',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sysemaillog',
            name='email_body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sysemaillog',
            name='mail_sent_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sysemaillog',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Sent'), ('0', 'Failed')], max_length=1),
        ),
        migrations.AlterField(
            model_name='sysemaillog',
            name='type',
            field=models.CharField(blank=True, choices=[('SR', 'Single Recipient'), ('MR', 'Multiple Recipient')], default='SR', max_length=2),
        ),
    ]
