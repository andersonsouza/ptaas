from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class OwnableMixin(models.Model):
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True


class ProccessAwareMixin(models.Model):
    pid = models.PositiveIntegerField('PID', null=True, blank=True)

    class Meta:
        abstract = True
