# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 17:19
from __future__ import unicode_literals

import api.fields
import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0064_session_bbscores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='bbscores',
            field=models.FileField(blank=True, max_length=255, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=api.fields.PathAndRename(prefix='bbscores')),
        ),
        migrations.AlterField(
            model_name='session',
            name='scoresheet',
            field=models.FileField(blank=True, max_length=255, null=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to=api.fields.PathAndRename(prefix='scoresheet')),
        ),
    ]