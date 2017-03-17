# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 15:41
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Q


def forwards(apps, schema_editor):
    Award = apps.get_model('app', 'Award')

    awards = Award.objects.filter(
        Q(
            kind__in=[
                31,
                32
            ],
            age=0,
            status=10,
            entity__kind__in=[
                11,
            ],
            entity__short_name__in=[
                'LOL',
                'MAD',
                'EVG',
                'FWD',
                'NED',
                'SWD',
            ],
            is_primary=True,
        ) |
        Q(
            kind__in=[
                31,
                32
            ],
            status=10,
            entity__kind__in=[
                1,
            ],
            entity__short_name__in=[
                'BHS',
            ],
            is_primary=True,
        )
    )

    for award in awards:
        qr = award.qualifier_rounds if award.qualifier_rounds else 2
        entities = award.entity.children.filter(
            kind__in=[
                11,
                21,
            ],
            status=10,
        )
        for entity in entities:
            new = Award(
                name="{0} Qualifier".format(award.name),
                status=0,
                kind=award.kind,
                age=award.age,
                championship_season=award.qualifier_season,
                championship_rounds=qr,
                is_primary=True,
                threshold=award.threshold,
                minimum=award.minimum,
                advance=award.advance,
                entity=entity,
                parent=award,
            )
            new.save()


def backwards(apps, schema_editor):
    Award = apps.get_model('app', 'Award')
    awards = Award.objects.exclude(parent=None)
    awards.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_award_parent'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
