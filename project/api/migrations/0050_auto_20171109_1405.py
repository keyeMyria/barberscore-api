# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-09 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_auto_20171109_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='mem_status',
            field=models.IntegerField(blank=True, choices=[(10, 'Active'), (20, 'Active Internal'), (30, 'Active Licensed'), (40, 'Cancelled'), (50, 'Closed'), (60, 'Closed Merged'), (70, 'Closed Revoked'), (80, 'Closed Voluntary'), (90, 'Expelled'), (100, 'Expired'), (105, 'Expired Licensed'), (110, 'Lapsed'), (120, 'Not Approved'), (130, 'Pending'), (140, 'Pending Voluntary'), (150, 'Suspended'), (160, 'Suspended Membership')], null=True),
        ),
    ]