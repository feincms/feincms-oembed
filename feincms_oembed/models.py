from datetime import datetime
import hashlib
import urllib2

from django.core.exceptions import ValidationError
from django.db import models


class CachedLookupManager(models.Manager):
    def request(self, url, max_age=24*60*60):
        lookup, created = self.get_or_create(
            hash=hashlib.sha1(url).hexdigest(),
            max_age_seconds=max_age,
            defaults={
                'url': url,
                })

        if created:
            lookup.clean()
            lookup.save()

        return lookup.response


class CachedLookup(models.Model):
    hash = models.CharField(max_length=40, unique=True)
    url = models.URLField(verify_exists=False, max_length=1000)
    _response = models.TextField(blank=True, null=True)
    _httpstatus = models.PositiveIntegerField(blank=True, null=True)

    max_age_seconds = models.PositiveIntegerField(default=24*60*60)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('cached lookup')
        verbose_name_plural = _('cached lookups')

    objects = CachedLookupManager()

    @property
    def response(self):
        delta = datetime.now() - self.modified

        if delta.seconds > self.max_age_seconds:
            self.clean()
            self.save()

        # http responses are always ascii. but django decodes the ascii bytestring
        # during saving. so we have to reencode, sometimes. (after the data was written to the db)
        response = self._response
        if type(response) == unicode:
            response = response.encode('utf-8')

        return response

    def clean(self, *args, **kwargs):
        try:
            request = urllib2.urlopen(self.url)
        except urllib2.URLError as e:
            raise ValidationError('This URL cannot be requested: %s', e)

        raw = request.read()

        try:
            decoded = raw.decode('utf-8')
        except UnicodeDecodeError:
            decoded = raw.decode('iso8859-1')
        self._response = decoded
        self._httpstatus = request.getcode()

    def __unicode__(self):
        return self.url
