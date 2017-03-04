# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20170218_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='level',
            field=models.IntegerField(blank=True, choices=[(0, 'International'), (1, 'District'), (2, 'Division'), (3, 'Chapter')], null=True),
        ),
    ]