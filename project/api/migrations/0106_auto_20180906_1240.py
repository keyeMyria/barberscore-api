# Generated by Django 2.0.8 on 2018-09-06 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0105_auto_20180906_1227'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='session',
            unique_together={('convention', 'kind')},
        ),
    ]
