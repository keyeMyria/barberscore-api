# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 02:37
from __future__ import unicode_literals

from django.db import migrations

def role_to_person(apps, schema_editor):
    Performer = apps.get_model("app", "Performer")
    for p in Performer.objects.all():
        try:
            p.tenor_new = p.tenor.person
        except AttributeError:
            pass
        try:
            p.lead_new = p.lead.person
        except AttributeError:
            pass
        try:
            p.baritone_new = p.baritone.person
        except AttributeError:
            pass
        try:
            p.bass_new = p.bass.person
        except AttributeError:
            pass
        try:
            p.director_new = p.director.person
        except AttributeError:
            pass
        try:
            p.codirector_new = p.codirector.person
        except AttributeError:
            pass
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170120_1825'),
    ]

    operations = [
        migrations.RunPython(role_to_person),
    ]