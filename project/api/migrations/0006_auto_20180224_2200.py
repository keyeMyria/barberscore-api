# Generated by Django 2.0.2 on 2018-02-25 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180224_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitor',
            name='is_archived',
        ),
        migrations.RemoveField(
            model_name='convention',
            name='is_archived',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='is_archived',
        ),
        migrations.RemoveField(
            model_name='round',
            name='is_archived',
        ),
        migrations.RemoveField(
            model_name='session',
            name='is_archived',
        ),
    ]
