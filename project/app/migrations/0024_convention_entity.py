# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20170219_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='entity',
            field=models.ForeignKey(blank=True, help_text='\n            The owning entity for the convention.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conventions', to='app.Entity'),
        ),
    ]