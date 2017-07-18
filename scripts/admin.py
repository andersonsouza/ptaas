from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.admin.widgets import AdminTextInputWidget
from django.db import models

from scripts.models import ScriptCategory, Script, Vulnerability, \
    VulnerabilityCategory, Trigger, TriggerParameter


@register(ScriptCategory)
class ScriptCategoryAdmin(admin.ModelAdmin):
    pass


@register(Script)
class ScriptAdmin(admin.ModelAdmin):

    list_display = ('name', 'category')


@register(VulnerabilityCategory)
class VulnerabilityCategoryAdmin(admin.ModelAdmin):
    pass


@register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'report_template_file')


class TriggerParameterInline(admin.TabularInline):
    
    model = TriggerParameter
    list_display = ('key', 'value')
    formfield_overrides = {
        models.TextField: {'widget': AdminTextInputWidget},
    }

@register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'script', 'match_type', 'match', 'run_script', 'parameters')
    
    inlines = [TriggerParameterInline, ]
