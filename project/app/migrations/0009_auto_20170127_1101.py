# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170126_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='kind',
            field=models.IntegerField(choices=[(b'International', [(1, b'Barbershop Harmony Society'), (2, b'Harmony Incorporated')]), (b'District', [(11, b'District'), (12, b'Noncompetitive'), (13, b'Affiliate')]), (b'Division', [(21, b'Division')]), (b'Group', [(31, b'Quartet'), (32, b'Chorus'), (33, b'Very Large Quartet')])], help_text=b'\n            The kind of organization.'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='level',
            field=models.IntegerField(choices=[(0, b'organization'), (1, b'District'), (2, b'Division'), (3, b'Group')]),
        ),
    ]
