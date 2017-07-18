from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.decorators import register
from django.shortcuts import redirect
from django.urls.base import reverse
from django.utils.safestring import mark_safe

from inspections.models import Inspection, InspectionVulnerability


@register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    '''Admin interface for inspection management.'''

    list_display = ('id', 'status', 'host', 'script', 'run_link')

    def run_link(self, obj):
        return mark_safe('<a href="%s">Run</a>' % reverse('admin:inspection_run', args=(obj.pk,)))

    def get_urls(self):
        urls = super(InspectionAdmin, self).get_urls()
        my_urls = [
            url(r'^run/([0-9]*)/$', self.run_view, name='inspection_run'),
        ]
        return my_urls + urls

    def run_view(self, request, pk):
        '''Execute the inspection specified by pk.'''
        try:
            Inspection.objects.get(pk=pk).run()
            self.message_user(request, 'Inspection prepared to execution.')
        except Exception as e:
            self.message_user(request, 'Fail to execute inspection: ' % e.message(), messages.ERROR)
        return redirect('/inspections/inspection/')


@register(InspectionVulnerability)
class InspectionVulnerabilityAdmin(admin.ModelAdmin):

    list_display = ('id', 'vulnerability_detected', 'inspection')
