# Generated by Django 2.0 on 2018-08-06 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_auto_20180728_0922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitor',
            old_name='csa_report',
            new_name='csa',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='oss_report',
            new_name='oss',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='sa_report',
            new_name='sa',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='oss_report',
            new_name='oss',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='sa_report',
            new_name='sa',
        ),
    ]
