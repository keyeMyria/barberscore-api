# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 16:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0138_session_datet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
    ]
