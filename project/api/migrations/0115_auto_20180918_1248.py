# Generated by Django 2.1.1 on 2018-09-18 19:48

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0114_auto_20180915_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appearance',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (7, 'Built'), (10, 'Started'), (20, 'Finished'), (25, 'Variance'), (30, 'Verified')], default=0, help_text='DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.'),
        ),
    ]
