from __future__ import unicode_literals

from django.db import models
from django.db.transaction import atomic
from django_extensions.db.models import TimeStampedModel

from common.models import OwnableMixin
from inspections.proccess import ProcessManager
from projects.models import Host, NetworkAddress
from scripts.models import Script, Vulnerability, Trigger


class Inspection(OwnableMixin, TimeStampedModel):

    STATUS_QUEUED = 1
    STATUS_RUNNING = 2
    STATUS_EXECUTED = 3
    STATUS_CANCELED = 4
    STATUS_FAILED = 5
    STATUS_CHOICES = (
        (1, 'Queued'),
        (2, 'Running'),
        (3, 'Executed'),
        (4, 'Canceled'),
        (5, 'Failed')
    )

    status = models.PositiveIntegerField('Status', choices=STATUS_CHOICES, default=STATUS_QUEUED)
    host = models.ForeignKey(Host, verbose_name='Target Host')
    network_addres = models.ForeignKey(NetworkAddress, verbose_name='Network Address', null=True, blank=True)
    script = models.ForeignKey(Script, verbose_name='Script')
    triggered_by = models.ForeignKey(Trigger, verbose_name='Triggered by', null=True, blank=True)
    output = models.TextField('Inspection Output', null=True, blank=True)

    class Meta:
        verbose_name = 'Host Inspection'
        verbose_name_plural = 'Host Inspections'

    def __str__(self):
        return '#%s %s: %s' % (self.pk, self.get_status_display(), self.host)

    @property
    def parameters(self):
        parameters =  self.triggered_by.parameters if (self.triggered_by) else {}
        parameters['host_fqdn'] = self.host.fqdn
        parameters['host_ip_address'] = self.network_addres.ip_address
        parameters['host_protocol'] = self.network_addres.protocol
        return parameters

    @property
    def command(self):
        return self.script.assemble_command(self.parameters)

    @atomic
    def run(self):
        '''Send the inspection to be executed by the Process Manager.'''
        command = self.script.assemble_command(self.parameters)
        process = ProcessManager.run(self.id, command, self.update_status)
        self.status = self.STATUS_RUNNING
        self.save()
        return process

    def update_status(self, process):
        '''Callback method to parse the process output and update the inspection status.'''
        output, error = process.communicate()
        self.status = self.STATUS_FAILED if error else self.STATUS_EXECUTED
        self.output = output
        self.save()
        for new_script in self.script.parse_output(output):
            if new_script['trigger'].associated_vulnerability:
                InspectionVulnerability.register(self, new_script['trigger'])
            if new_script['script']:
                new_inspection = Inspection.objects.create(
                    owner = self.owner,
                    host = self.host,
                    network_addres = self.network_addres,
                    script = new_script['script'],
                    triggered_by = new_script['trigger'],
                )
                new_inspection.run()


class InspectionVulnerability(TimeStampedModel):
    
    inspection = models.ForeignKey(Inspection, verbose_name='Inspection')
    vulnerability_detected = models.ForeignKey(Vulnerability, verbose_name='Vulnerability Detected')
    extended_data = models.TextField('Extended Data', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Vulnerability detected by inspection'
        verbose_name_plural = 'Vulnerabilities detectedd by inspection'

    def __str__(self):
        return '#%s: %s' % (self.pk, self.vulnerability_detected)
    
    @staticmethod
    def register(inspection, trigger, extended_data=None):
        already_detected = InspectionVulnerability.objects.filter(
            inspection=inspection,
            vulnerability_detected=trigger.associated_vulnerability
        ).exists()
        if not already_detected:
            detected = InspectionVulnerability.objects.create(
                inspection=inspection,
                vulnerability_detected=trigger.associated_vulnerability,
                extended_data=extended_data
            )
            return detected
