# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_auto_20170818_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.Person'),
        ),
    ]
