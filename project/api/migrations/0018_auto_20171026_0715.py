# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 14:15
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_member_is_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (5, 'Invited'), (7, 'Withdrawn'), (10, 'Submitted'), (20, 'Approved'), (52, 'Scratched'), (55, 'Disqualified'), (57, 'Final'), (95, 'Archived')], default=0),
        ),
    ]