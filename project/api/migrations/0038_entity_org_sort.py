# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0037_auto_20170620_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='org_sort',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]