# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_officer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='nomen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
