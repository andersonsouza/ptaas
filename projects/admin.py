from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models

from projects.models import Project, Host, NetworkAdress


@register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'status')


class NetworkAddressInline(admin.TabularInline):

    model = NetworkAdress
    list_display = ('protocol', 'ip_address')
    formfield_overrides = {
        models.TextField: {'widget': AdminTextInputWidget},
    }


@register(Host)
class HostAdmin(admin.ModelAdmin):

    list_display = ('name', 'fqnd')
    inlines = [NetworkAddressInline, ]


@register(NetworkAdress)
class NetworkAddressAdmin(admin.ModelAdmin):

    list_display = ('ip_address', 'protocol')
