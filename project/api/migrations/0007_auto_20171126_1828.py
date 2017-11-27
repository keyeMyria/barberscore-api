# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171126_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='gender',
            field=models.IntegerField(choices=[(10, 'Male'), (20, 'Female'), (30, 'Mixed')], default=10, help_text='\n            The gender of group.\n        '),
        ),
        migrations.AddField(
            model_name='session',
            name='gender',
            field=models.IntegerField(choices=[(10, 'Male'), (20, 'Female'), (30, 'Mixed')], default=10, help_text='\n            The gender of session.\n        '),
        ),
    ]
