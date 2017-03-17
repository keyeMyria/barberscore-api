# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 15:41
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Award = apps.get_model('app', 'Award')
    awards = Award.objects.exclude(parent=None)
    awards.delete()


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20170317_0603'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
