# Generated by Django 2.0.7 on 2018-07-04 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20180704_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='csa_report',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
