from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel


class ScriptCategory(models.Model):

    category = models.CharField('Script Category', max_length=50, help_text='Script category name.')

    class Meta:
        verbose_name = 'Script Category'
        verbose_name_plural = 'Script Categories'


class Script(TimeStampedModel):

    category = models.ForeignKey(ScriptCategory, verbose_name='Category of the script.')
    name = models.CharField('Script name', max_length=100)
    code = models.TextField('Script code')


class VulnerabilityCategory(models.Model):

    category = models.CharField('Vulnerability Category', max_length=50, help_text='Script category name.')

    class Meta:
        verbose_name = 'Vulnerability Category'
        verbose_name_plural = 'Vulnerability Categories'


class Vulnerability(TimeStampedModel):

    category = models.ForeignKey(VulnerabilityCategory, verbose_name='Category of the vulnerability')
    name = models.CharField('Vulnerability', max_length=100)
    description = models.TextField('Description', null=True, blank=True)
    report_template_file = models.CharField('Report template file', max_length=50)

    class Meta:
        verbose_name = 'Vulnerability'
        verbose_name_plural = 'Vulnerabilities'
