# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 05:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20170217_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='songscore',
            name='song_ptr',
        ),
        migrations.DeleteModel(
            name='SongScore',
        ),
    ]