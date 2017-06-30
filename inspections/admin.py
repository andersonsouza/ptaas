from django.contrib import admin
from django.contrib.admin.decorators import register

from inspections.models import HostInspection, HostInspectionVulnerability


@register(HostInspection)
class HostInspectionAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'host', 'script')


@register(HostInspectionVulnerability)
class HostInspectionVulnerabilityAdmin(admin.ModelAdmin):

    list_display = ('id', 'vulnerability_detected', 'host_inspection')
