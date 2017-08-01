# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NetworkAdress',
            new_name='NetworkAddress',
        ),
        migrations.AlterModelOptions(
            name='networkaddress',
            options={'verbose_name': 'Network Address', 'verbose_name_plural': 'Network Addresses'},
        ),
        migrations.RemoveField(
            model_name='host',
            name='fqnd',
        ),
        migrations.AddField(
            model_name='host',
            name='fqdn',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='FQDN'),
        ),
    ]
