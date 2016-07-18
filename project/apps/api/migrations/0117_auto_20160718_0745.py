# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_auto_20160717_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='performance',
            options={},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={},
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter',
            field=models.ForeignKey(blank=True, help_text=b'Chapter is reserved for Choruses only.  Do NOT add chapter for quartet', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='api.Chapter'),
        ),
    ]
