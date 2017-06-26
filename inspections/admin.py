from django.contrib import admin
from django.contrib.admin.decorators import register

from inspections.models import HostInspection, HostInspectionVulnerability


@register(HostInspection)
class HostInspectionAdmin(admin.ModelAdmin):
    pass


@register(HostInspectionVulnerability)
class HostInspectionVulnerabilityAdmin(admin.ModelAdmin):
    pass
