from django.contrib import admin
from django.contrib.admin.decorators import register

from scripts.models import ScriptCategory, Script, Vulnerability, \
    VulnerabilityCategory, Trigger


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


@register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'script', 'match_type', 'match', 'run_script', 'parameters')
