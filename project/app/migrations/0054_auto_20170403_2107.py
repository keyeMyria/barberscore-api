# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20170403_2024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='repertory',
            unique_together=set([('entity', 'catalog')]),
        ),
    ]
