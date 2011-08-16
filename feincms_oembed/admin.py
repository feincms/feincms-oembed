from django.contrib import admin

from feincms_oembed.models import CachedLookup

class CachedLookupAdmin(admin.ModelAdmin):
    list_display = ('url', 'created', 'modified', 'max_age_seconds', '_httpstatus')
    fields = ('hash', 'url', 'max_age_seconds', '_httpstatus', '_response')
    readonly_fields = ('_response', '_httpstatus')

admin.site.register(CachedLookup, CachedLookupAdmin)