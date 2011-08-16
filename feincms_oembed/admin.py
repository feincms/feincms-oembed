from django.contrib import admin

from feincms_oembed.models import LookupCached

class LookupCachedAdmin(admin.ModelAdmin):
    list_display = ('url', 'created', 'modified', 'max_age_seconds', '_httpstatus')
    fields = ('url', 'max_age_seconds', '_httpstatus', '_response')
    readonly_fields = ('_response', '_httpstatus')

admin.site.register(LookupCached, LookupCachedAdmin)