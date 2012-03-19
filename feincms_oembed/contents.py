from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms_oembed.models import CachedLookup


class OembedContent(models.Model):
    """
    Content type for integrating anything supported by the oembed provider into the CMS

    Usage::

        Page.create_content_type(OembedContent, TYPE_CHOICES=[
            ('default', _('Default presentation'), {'maxwidth': 500, 'maxheight': 300}),
            ('transparent, _('Transparent'), {'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
            ])
    """

    url = models.URLField(_('URL'), help_text=_('Paste here any URL from supported external websites. F.e. a Youtube Video will be: http://www.youtube.com/watch?v=Nd-vBFJN_2E, a Vimeo Video will be http://vimeo.com/16090755 or a soundcloud audio file: http://soundcloud.com/feinheit/focuszone-radio-spot more sites: http://api.embed.ly/'))

    class Meta:
        abstract = True
        verbose_name = _('External content')
        verbose_name_plural = _('External contents')

    @classmethod
    def initialize_type(cls, TYPE_CHOICES):
        choices = [row[0:2] for row in TYPE_CHOICES]
        cls.add_to_class('type', models.CharField(_('type'), max_length=20,
            choices=choices, default=choices[0][0]))

        cls._type_config = dict((row[0], row[2]) for row in TYPE_CHOICES)

    def get_html_from_json(self, fail_silently=False):
        params = self._type_config.get(self.type, {})

        try:
            embed = CachedLookup.objects.oembed(self.url, **params)
        except TypeError:
            if fail_silently:
                return u''
            raise ValidationError('The specified URL %s cannot be used with embed.ly' % self.url)

        return render_to_string((
            'external/%s.html' % embed.get('type', 'default'),
            'external/default.html',
            ), {'response': embed, 'content': self})

    def clean(self, *args, **kwargs):
        self.get_html_from_json()

    def render(self, **kwargs):
        return self.get_html_from_json(fail_silently=True)


class FeedContent(models.Model):
    url = models.URLField(_('Feed URL'), help_text=_('Paste here any RSS Feed URL. F.e. https://www.djangoproject.com/rss/weblog/'))

    class Meta:
        abstract = True
        verbose_name = _('RSS Feed')
        verbose_name_plural = _('RSS Feeds')

    def clean(self, *args, **kwargs):
        import feedparser
        
        response = CachedLookup.objects.request(self.url, 30*60)
        result = feedparser.parse(response)

        # no feed validation at this time
        #if response._httpstatus != 200:
        #    raise ValidationError('Feed could not be parsed (HTTP Status: %s): %s'
        #                          % (result.get('status', '?'),
        #                             result.get('bozo_exception', 'no exception specified')))

    @property
    def feed(self):
        import feedparser

        return feedparser.parse(CachedLookup.objects.request(self.url, 30*60))

    def render(self, **kwargs):
        return render_to_string('content/external/feed.html',
                                {'feed' : self.feed})

