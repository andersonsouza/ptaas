# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Script name')),
                ('code', models.TextField(verbose_name='Script code')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScriptCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='Script category name.', max_length=50, verbose_name='Script Category')),
            ],
            options={
                'verbose_name': 'Script Category',
                'verbose_name_plural': 'Script Categories',
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_type', models.PositiveIntegerField(choices=[(0, 'Null/empty values'), (1, 'Any non null/empty values'), (2, 'The specified integer value'), (3, 'The specified string'), (4, 'Matches against a RegEx pattern')], default=4, verbose_name='Match type')),
                ('match', models.TextField(blank=True, null=True, verbose_name='Match Pattern')),
            ],
            options={
                'verbose_name': 'Script Trigger',
                'verbose_name_plural': 'Script Triggers',
            },
        ),
        migrations.CreateModel(
            name='TriggerParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(max_length=100, verbose_name='Parameter Key')),
                ('value', models.TextField(max_length=1000, verbose_name='Parameter Value')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_set', to='scripts.Trigger', verbose_name='Trigger')),
            ],
            options={
                'verbose_name': 'Trigger Parameter',
                'verbose_name_plural': 'Triggers Parameters',
            },
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Vulnerability')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('report_template_file', models.CharField(max_length=50, verbose_name='Report template file')),
            ],
            options={
                'verbose_name': 'Vulnerability',
                'verbose_name_plural': 'Vulnerabilities',
            },
        ),
        migrations.CreateModel(
            name='VulnerabilityCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='Script category name.', max_length=50, verbose_name='Vulnerability Category')),
            ],
            options={
                'verbose_name': 'Vulnerability Category',
                'verbose_name_plural': 'Vulnerability Categories',
            },
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scripts.VulnerabilityCategory', verbose_name='Category of the vulnerability'),
        ),
        migrations.AddField(
            model_name='trigger',
            name='associated_vulnerability',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scripts.Vulnerability', verbose_name='Associated Vulnerability'),
        ),
        migrations.AddField(
            model_name='trigger',
            name='run_script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggeredby_set', to='scripts.Script', verbose_name='Run script'),
        ),
        migrations.AddField(
            model_name='trigger',
            name='script',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trigger_set', to='scripts.Script', verbose_name='Caller Script'),
        ),
        migrations.AddField(
            model_name='script',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scripts.ScriptCategory', verbose_name='Category of the script.'),
        ),
        migrations.AlterUniqueTogether(
            name='triggerparameter',
            unique_together=set([('trigger', 'key')]),
        ),
    ]
