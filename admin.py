from django.contrib import admin

from models import LookupCached

class LookupCachedAdmin(admin.ModelAdmin):
    list_display = ('url', 'created', 'modified', 'max_age_seconds')

admin.site.register(LookupCached, LookupCachedAdmin)