# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 22:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0093_auto_20170716_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='api.Entity'),
        ),
        migrations.AlterField(
            model_name='convention',
            name='entity',
            field=models.ForeignKey(blank=True, help_text='\n            The owning entity for the convention.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conventions', to='api.Entity'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='api.Entity'),
        ),
        migrations.AlterField(
            model_name='member',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.Entity'),
        ),
        migrations.AlterField(
            model_name='officer',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='officers', to='api.Entity'),
        ),
        migrations.AlterField(
            model_name='repertory',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='repertories', to='api.Entity'),
        ),
    ]