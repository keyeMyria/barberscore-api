# Generated by Django 2.0 on 2018-08-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_competitor_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='participants',
            field=models.CharField(blank=True, default='', help_text='Director(s) or Members (listed TLBB)', max_length=255),
        ),
        migrations.AddField(
            model_name='competitor',
            name='representing',
            field=models.CharField(blank=True, default='', help_text='Representing entity', max_length=255),
        ),
    ]
