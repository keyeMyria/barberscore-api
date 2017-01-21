# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 02:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170115_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='performer',
            name='baritone_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_baritone_new', to='app.Person'),
        ),
        migrations.AddField(
            model_name='performer',
            name='bass_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_bass_new', to='app.Person'),
        ),
        migrations.AddField(
            model_name='performer',
            name='codirector_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_codirector_new', to='app.Person'),
        ),
        migrations.AddField(
            model_name='performer',
            name='director_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_director_new', to='app.Person'),
        ),
        migrations.AddField(
            model_name='performer',
            name='lead_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_lead_new', to='app.Person'),
        ),
        migrations.AddField(
            model_name='performer',
            name='tenor_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performers_tenor_new', to='app.Person'),
        ),
    ]