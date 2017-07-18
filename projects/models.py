from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

from common.models import OwnableMixin


class Project(OwnableMixin, TimeStampedModel):

    STATUS_NEW = 1
    STATUS_DOING = 2
    STATUS_ENDED = 3

    STATUS_CHOICES = (
        (1, 'New'),
        (2, 'Doing'),
        (3, 'Ended'),
    )

    name = models.CharField('Project Name', max_length=100)
    status = models.PositiveIntegerField('Status', choices=STATUS_CHOICES, default=STATUS_NEW)

    def __str__(self):
        return self.name


class Host(TimeStampedModel):

    project = models.ForeignKey(Project, verbose_name='Project')
    name = models.CharField('Host Name', max_length=100)
    description = models.TextField('Host Description', null=True, blank=True)
    fqdn = models.CharField('FQDN', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name

    @property
    def addresses(self):
        return self.networkaddress_set.all()


class NetworkAddress(models.Model):

    PROTOCOL_IPV4 = 4
    PROTOCOL_IPV6 = 6

    PROTOCOL_CHOICES = (
        (4, 'IPv4'),
        (6, 'IPv6'),
    )

    protocol = models.PositiveIntegerField('Protocol', choices=PROTOCOL_CHOICES, default=PROTOCOL_IPV4)
    ip_address = models.GenericIPAddressField('IP Address')
    host = models.ForeignKey(Host, verbose_name='Host')

    class Meta:
        verbose_name = 'Network Address'
        verbose_name_plural = 'Network Addresses'

    def __str__(self):
        return '%s: %s' % (self.get_protocol_display(), self.ip_address)
