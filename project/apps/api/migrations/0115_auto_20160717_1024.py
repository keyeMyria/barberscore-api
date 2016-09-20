# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 17:24
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0114_performer_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='district',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='district_groups', to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='group',
            name='division',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='division_groups', to='api.Organization'),
        ),
    ]