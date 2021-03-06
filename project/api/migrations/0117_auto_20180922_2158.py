# Generated by Django 2.1.1 on 2018-09-23 04:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0116_auto_20180920_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='asterisks',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='song',
            name='dixons',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='song',
            name='legacy_chart',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
