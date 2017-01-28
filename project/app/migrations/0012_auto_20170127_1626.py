# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 00:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170127_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='app.Entity'),
        ),
        migrations.AddField(
            model_name='award',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='awards', to='app.Entity'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chapters', to='app.Entity'),
        ),
        migrations.AddField(
            model_name='convention',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conventions', to='app.Entity'),
        ),
        migrations.AddField(
            model_name='host',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hosts', to='app.Entity'),
        ),
        migrations.AddField(
            model_name='judge',
            name='entity',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='judges', to='app.Entity'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='organization',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conventions', to='app.Organization'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='level',
            field=models.IntegerField(choices=[(0, b'Organization'), (1, b'District'), (2, b'Division'), (3, b'Group')]),
        ),
    ]
