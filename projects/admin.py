from django.contrib import admin
from django.contrib.admin.decorators import register

from projects.models import Project, Host, NetworkAdress


@register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'status')


@register(Host)
class HostAdmin(admin.ModelAdmin):

    list_display = ('name', 'fqnd')


@register(NetworkAdress)
class NetworkAddressAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'protocol')
