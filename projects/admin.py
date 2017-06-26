from django.contrib import admin
from django.contrib.admin.decorators import register

from projects.models import Project, Host, NetworkAdress


@register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@register(Host)
class HostAdmin(admin.ModelAdmin):
    pass


@register(NetworkAdress)
class NetworkAddressAdmin(admin.ModelAdmin):
    pass
