# Generated by Django 2.0.3 on 2018-03-17 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180317_1308'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name_plural': 'groups'},
        ),
        migrations.AlterModelOptions(
            name='office',
            options={'ordering': ['code']},
        ),
        migrations.AlterField(
            model_name='office',
            name='code',
            field=models.IntegerField(blank=True, choices=[('International', [(100, 'SCJC Chair'), (110, 'SCJC Chair Past'), (120, 'SCJC CA'), (130, 'SCJC MUS'), (140, 'SCJC PER'), (150, 'SCJC SNG'), (160, 'SCJC Chart'), (170, 'SCJC Admin')]), ('District', [(210, 'DRCJ'), (220, 'DRCJ Assistant'), (230, 'JUDGE CA'), (240, 'JUDGE MUS'), (250, 'JUDGE PER'), (260, 'JUDGE SNG')]), ('Group', [(310, 'CPRES'), (320, 'CSEC'), (320, 'CDIR'), (340, 'CASS'), (350, 'CMAN'), (410, 'QADM')])], help_text='\n            The short-form office code.', null=True),
        ),
    ]
