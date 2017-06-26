from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

from common.models import OwnableMixin, ProccessAwareMixin
from projects.models import Host
from scripts.models import Script, Vulnerability


class HostInspection(OwnableMixin, ProccessAwareMixin, TimeStampedModel):

    STATUS_QUEUED = 1
    STATUS_RUNNING = 2
    STATUS_EXECUTED = 3
    STATUS_CANCELED = 4
    STATUS_CHOICES = (
        (1, 'Queued'),
        (2, 'Running'),
        (3, 'Executed'),
        (4, 'Canceled')
    )

    status = models.PositiveIntegerField('Status', choices=STATUS_CHOICES, default=STATUS_QUEUED)
    host = models.ForeignKey(Host, verbose_name='Target Host')
    script = models.ForeignKey(Script, verbose_name='Executed Script')
    
    class Meta:
        verbose_name = 'Host Inspection'
        verbose_name_plural = 'Host Inspections'


class HostInspectionVulnerability(TimeStampedModel):
    
    host_inspection = models.ForeignKey(HostInspection, verbose_name='Host Inspection')
    vulnerability_detected = models.ForeignKey(Vulnerability, verbose_name='Vulnerability Detected')
    extended_data = models.TextField('Extended Data')
    
    class Meta:
        verbose_name = 'Vulnerability detected by host inspection'
        verbose_name_plural = 'Vulnerabilities detectedd by host inspection'
