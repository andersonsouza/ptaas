from __future__ import unicode_literals

from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel


class ScriptCategory(models.Model):

    category = models.CharField('Script Category', max_length=50, help_text='Script category name.')

    class Meta:
        verbose_name = 'Script Category'
        verbose_name_plural = 'Script Categories'

    def __str__(self):
        return self.category


class Script(TimeStampedModel):

    category = models.ForeignKey(ScriptCategory, verbose_name='Category of the script.')
    name = models.CharField('Script name', max_length=100)
    code = models.TextField('Script code')

    def __str__(self):
        return self.name

    def assemble_command(self, params={}):
        try :
            return self.code % params
        except:
            raise Exception('Fail to assemble command: Invalid parameters.')

    def parse_output(self, output):
        new_scripts = []
        for trigger in self.trigger_set.all():
            script = trigger.parse_output(output)
            if script:
                new_scripts.append(script)
                if script['script']:
                    print('[%s] New script triggered: %s' 
                          % (datetime.now().strftime('%d/%b/%Y %H:%M:%S'), script['script'].code))
        return new_scripts


class VulnerabilityCategory(models.Model):

    category = models.CharField('Vulnerability Category', max_length=50, help_text='Script category name.')

    class Meta:
        verbose_name = 'Vulnerability Category'
        verbose_name_plural = 'Vulnerability Categories'

    def __str__(self):
        return self.category


class Vulnerability(TimeStampedModel):

    category = models.ForeignKey(VulnerabilityCategory, verbose_name='Category of the vulnerability')
    name = models.CharField('Vulnerability', max_length=100)
    description = models.TextField('Description', null=True, blank=True)
    report_template_file = models.CharField('Report template file', max_length=50)

    class Meta:
        verbose_name = 'Vulnerability'
        verbose_name_plural = 'Vulnerabilities'

    def __str__(self):
        return self.name


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
    run_script = models.ForeignKey(Script, verbose_name='Run script', related_name='triggeredby_set', null=True, blank=True)
    associated_vulnerability = models.ForeignKey(Vulnerability, verbose_name='Associated Vulnerability', null=True, blank=True)

    class Meta:
        verbose_name = 'Script Trigger'
        verbose_name_plural = 'Script Triggers'

    def __str__(self):
        return '%s: %s' % (self.get_match_type_display(), self.match or '')

    @property
    def parameters(self):
        parameters = {}
        for parameter in self.parameter_set.all():
            parameters.update({parameter.key: parameter.value})
        return parameters

    def __parse_output_null(self, output):
        return True if (output == None) else False

    def __parse_output_not_null(self, output):
        return False if (output == None) else True

    def __parse_output_integer_value(self, output):
        return True if (self.match == output) else False

    def __parse_output_string(self, output):
        return True if (self.match in output) else False

    def __parse_output_regex(self, output):
        try:
            r = RegexValidator(self.match)
            r(output)
            return True
        except:
            return False
        
        # return True if (Regex(self.match).parseString(output)) else False

    def parse_output(self, output):
        if self.match_type == self.MATCH_NULL:
            match = self.__parse_output_null(output)
        elif self.match_type == self.MATCH_NOT_NULL:
            match = self.__parse_output_not_null(output)
        elif self.match_type == self.MATCH_INTEGER_VALUE:
            match = self.__parse_output_integer_value(output)
        elif self.match_type == self.MATCH_STRING:
            match = self.__parse_output_string(output)
        elif self.match_type == self.MATCH_REGEX:
            match = self.__parse_output_regex(output)
        else:
            raise Exception('Invalid Match Type: %s' % self.match_type)

        return {'script': self.run_script or None, 'parameters': self.parameters, 'trigger': self} if match else None


class TriggerParameter(models.Model):

    trigger = models.ForeignKey(Trigger, verbose_name='Trigger', related_name='parameter_set')
    key = models.TextField('Parameter Key', max_length=100)
    value = models.TextField('Parameter Value', max_length=1000)

    class Meta:
        verbose_name = 'Trigger Parameter'
        verbose_name_plural = 'Triggers Parameters'
        unique_together = ('trigger', 'key')

    def __str__(self):
        return '%s: %s' % (self.key, self.value)
