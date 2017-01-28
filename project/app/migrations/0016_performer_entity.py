# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 13:13
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20170127_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='performer',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers', to='app.Entity'),
        ),
    ]
