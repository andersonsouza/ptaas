# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0002_auto_20170705_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='pid',
        ),
        migrations.AddField(
            model_name='inspection',
            name='output',
            field=models.TextField(blank=True, null=True, verbose_name='Inspection Output'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Queued'), (2, 'Running'), (3, 'Executed'), (4, 'Canceled'), (5, 'Failed')], default=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='inspectionvulnerability',
            name='extended_data',
            field=models.TextField(blank=True, null=True, verbose_name='Extended Data'),
        ),
    ]
