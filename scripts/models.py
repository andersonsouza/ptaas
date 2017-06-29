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


class Trigger(models.Model):

    MATCH_NULL = 0
    MATCH_NOT_NULL = 1
    MATCH_INTEGER_VALUE = 2
    MATCH_STRING = 3
    MATCH_REGEX = 4

    MATCH_CHOICES = (
        (MATCH_NULL, 'Null/empty values'),
        (MATCH_NOT_NULL, 'Any non null/empty values'),
        (MATCH_INTEGER_VALUE, 'The specified integer value'),
        (MATCH_STRING, 'The specified string'),
        (MATCH_REGEX, 'Matches against a RegEx pattern'),
    )

    script = models.ForeignKey(Script, verbose_name='Caller Script', related_name='trigger_set')
    match_type = models.PositiveIntegerField('Match type', choices=MATCH_CHOICES, default=MATCH_REGEX)
    match = models.TextField('Match Pattern', null=True, blank=True)
    run_script = models.ForeignKey(Script, verbose_name='Run script', related_name='triggeredby_set')
    run_parameters = models.TextField('Run parameters')
    associated_vulnerability = models.ForeignKey(Vulnerability, verbose_name='Associated Vulnerability', null=True, blank=True)

    class Meta:
        verbose_name = 'Script Trigger'
        verbose_name_plural = 'Script Triggers'
