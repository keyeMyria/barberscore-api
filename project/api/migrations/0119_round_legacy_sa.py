# Generated by Django 2.1.1 on 2018-09-24 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0118_merge_20180923_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='legacy_sa',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
