# Generated by Django 2.0.6 on 2018-06-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_round_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='footnotes',
            field=models.TextField(blank=True, help_text='\n            Freeform text field; will print on OSS.'),
        ),
    ]
