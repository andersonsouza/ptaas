from django.contrib import admin
from django.contrib.admin.decorators import register

from inspections.models import Inspection, InspectionVulnerability


@register(Inspection)
class InspectionAdmin(admin.ModelAdmin):

    list_display = ('id', 'status', 'host', 'script')


@register(InspectionVulnerability)
class InspectionVulnerabilityAdmin(admin.ModelAdmin):

    list_display = ('id', 'vulnerability_detected', 'inspection')
