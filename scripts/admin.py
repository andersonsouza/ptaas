from django.contrib import admin
from django.contrib.admin.decorators import register

from scripts.models import ScriptCategory, Script, Vulnerability, \
    VulnerabilityCategory


@register(ScriptCategory)
class ScriptCategoryAdmin(admin.ModelAdmin):
    pass


@register(Script)
class ScriptAdmin(admin.ModelAdmin):
    pass


@register(VulnerabilityCategory)
class VulnerabilityCategoryAdmin(admin.ModelAdmin):
    pass


@register(Vulnerability)
class VulnerabilityAdmin(admin.ModelAdmin):
    pass
