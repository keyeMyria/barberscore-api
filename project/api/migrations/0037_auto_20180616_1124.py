# Generated by Django 2.0.6 on 2018-06-16 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_remove_contest_champion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='champ',
            new_name='champion',
        ),
    ]
