# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0080_auto_20170710_0913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='office',
            old_name='is_ml',
            new_name='is_cm',
        ),
    ]
