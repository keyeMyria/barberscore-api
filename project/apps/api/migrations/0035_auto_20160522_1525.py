# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 22:25
from __future__ import unicode_literals

from django.db import migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20160521_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(help_text=b'\n            The local timezone of the venue.'),
        ),
    ]
