from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from urllib import urlopen

from models import LookupCached

class OembedContent(models.Model):
    url = models.URLField()
    
    class Meta:
        abstract = True
        verbose_name = _('External content')
        verbose_name_plural = _('External contents')
    
    @classmethod
    def initialize_type(cls, PARAM_CHOICES=None):
        if PARAM_CHOICES is None:
            cls.add_to_class('parameters', models.CharField(max_length=50, 
                                                    blank=True, null=True))
        else:
            cls.add_to_class('parameters', models.CharField(max_length=50,
                                            choices=PARAM_CHOICES, 
                                            default=PARAM_CHOICES[0][0]))
    
    def get_html_from_json(self):
        oohembed_url = 'http://api.embed.ly/1/oembed?url=%s&%s' % (urlquote(self.url), self.parameters)
        
        lookup, created = LookupCached.objects.get_or_create(url=oohembed_url)
        
        try:
            json = simplejson.loads(lookup.response)
            type = json.get('type')
        except simplejson.JSONDecodeError:
            raise ValidationError('The specified url %s does not respond oembed json' % oohembed_url)
        
        return render_to_string(('external/%s.html' % type, 'external/default.html'), {'response' : json})
    
    def save(self, *args, **kwargs):
        self.get_html_from_json()
        super(OembedContent, self).save(*args, **kwargs)
    
    def render(self, request, context, **kwargs):
        return self.get_html_from_json()
    
