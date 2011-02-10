from datetime import datetime

from django.db import models

from urllib import urlopen

class LookupCached(models.Model):
    url = models.URLField(verify_exists=False, unique=True)
    _response = models.TextField(blank=True, null=True)
    
    max_age_seconds = models.PositiveIntegerField(default=24*60*60)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    @property
    def response(self):
        delta = datetime.now() - self.modified
        if delta.seconds > self.max_age_seconds:
            self.save()
        
        return self._response
    
    def save(self, *args, **kwargs):
        request = urlopen(self.url)
        self._response = request.read()
        super(LookupCached, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.url