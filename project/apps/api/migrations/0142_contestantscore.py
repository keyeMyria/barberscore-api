# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-23 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0141_auto_20160723_0657'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestantScore',
            fields=[
                ('contestant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Contestant')),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('mus_points', models.IntegerField(blank=True, null=True)),
                ('prs_points', models.IntegerField(blank=True, null=True)),
                ('sng_points', models.IntegerField(blank=True, null=True)),
                ('total_points', models.IntegerField(blank=True, null=True)),
                ('mus_score', models.FloatField(blank=True, null=True)),
                ('prs_score', models.FloatField(blank=True, null=True)),
                ('sng_score', models.FloatField(blank=True, null=True)),
                ('total_score', models.FloatField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('api.contestant',),
        ),
    ]