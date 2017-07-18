from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.decorators import register
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls.base import reverse
from django.utils.safestring import mark_safe

from inspections.models import Inspection
from projects.models import Project, Host, NetworkAddress


@register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'status', 'action_links')
    
    def action_links(self, obj):
        links = '%s | %s | %s | %s'
        details_link = '<a href="%s">Details</a>' % reverse('admin:project_details', args=(obj.pk,))
        run_link = '<a href="%s">Run Tests</a>' % reverse('admin:project_run', args=(obj.pk,))
        detect_link = '<a href="javascript:alert(\'Not implemented yet!\');">Detect Enviroment</a>'
        clone_link = '<a href="javascript:alert(\'Not implemented yet!\');">Clone Enviroment</a>'
        return mark_safe(links % (details_link, run_link, detect_link, clone_link))
    action_links.short_description = 'Actions'
    
    def get_urls(self):
        urls = super(ProjectAdmin, self).get_urls()
        my_urls = [
            url(r'^run/([0-9]*)/$', self.run_view, name='project_run'),
            url(r'^details/([0-9]*)/$', self.details_view, name='project_details'),
        ]
        return my_urls + urls
    
    def run_view(self, request, pk):
        '''Execute the entire project test.'''
        project = get_object_or_404(Project, pk=pk)
        try:
            for inspection in Inspection.objects.filter(host__project=project).all():
                inspection.run()
            project.status = Project.STATUS_DOING 
            project.save()
            self.message_user(request, 'Project execution started. Please be patient.')
        except Exception as e:
            self.message_user(request, 'Fail to execute project.: %s' % e.message(), level=messages.ERROR)
        return redirect('/projects/project/details/%s/' % pk)
    
    def details_view(self, request, pk):
        raise Exception('Not implemented yet...')
                    


class NetworkAddressInline(admin.TabularInline):

    model = NetworkAddress
    list_display = ('protocol', 'ip_address')
    formfield_overrides = {
        models.TextField: {'widget': AdminTextInputWidget},
    }


@register(Host)
class HostAdmin(admin.ModelAdmin):

    list_display = ('name', 'fqdn')
    inlines = [NetworkAddressInline, ]


@register(NetworkAddress)
class NetworkAddressAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'protocol')
