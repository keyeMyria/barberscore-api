# Generated by Django 2.0.7 on 2018-07-27 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_contest_is_primary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='footnote',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_improved',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_invitational',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_later',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_manual',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_multi',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_primary',
        ),
        migrations.RemoveField(
            model_name='award',
            name='is_rep_qualifies',
        ),
    ]
