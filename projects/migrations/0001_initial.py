# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 02:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Host Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Host Description')),
                ('fqnd', models.CharField(blank=True, max_length=100, null=True, verbose_name='FQND')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NetworkAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.PositiveIntegerField(choices=[(4, 'IPv4'), (6, 'IPv6')], default=4, verbose_name='Protocol')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Address')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Host', verbose_name='Host')),
            ],
            options={
                'verbose_name': 'Network Address',
                'verbose_name_plural': 'Network Adresses',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('status', models.PositiveIntegerField(choices=[(1, 'New'), (2, 'Doing'), (3, 'Ended')], default=1, verbose_name='Status')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='host',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project', verbose_name='Project'),
        ),
    ]
