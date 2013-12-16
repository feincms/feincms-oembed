import json

from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from feincms_oembed.models import CachedLookup


class OembedContent(models.Model):
    """
    Content type for integrating anything supported by the oembed provider into
    the CMS

    Usage::

        Page.create_content_type(OembedContent, TYPE_CHOICES=[
            ('default', _('Default presentation'), {
                'maxwidth': 500, 'maxheight': 300}),
            ('transparent', _('Transparent'), {
                'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
            ])
    """

    url = models.URLField(
        _('URL'),
        help_text=_(
            'Insert an URL to an external content you want to embed,'
            ' f.e. http://www.youtube.com/watch?v=Nd-vBFJN_2E'),
    )

    class Meta:
        abstract = True
        verbose_name = _('external content')
        verbose_name_plural = _('external contents')

    @classmethod
    def initialize_type(cls, TYPE_CHOICES, PARAMS={}):
        choices = [row[0:2] for row in TYPE_CHOICES]
        cls.add_to_class(
            'type',
            models.CharField(
                _('type'),
                max_length=20,
                choices=choices,
                default=choices[0][0],
            )
        )
        cls._type_config = dict((row[0], row[2]) for row in TYPE_CHOICES)
        cls._params = PARAMS

    def get_html_from_json(self, fail_silently=False):
        params = self._type_config.get(self.type, {})
        params.update(self._params)

        try:
            embed = CachedLookup.objects.oembed(self.url, **params)
        except TypeError:
            if fail_silently:
                return u''
            raise ValidationError(
                _('I don\'t know how to embed %s.') % self.url)

        return render_to_string((
            'content/external/%s.html' % embed.get('type'),
            'content/external/%s.html' % self.type,
            'content/external/default.html',
        ), {'response': embed, 'content': self})

    def clean(self, *args, **kwargs):
        self.get_html_from_json()

    def render(self, **kwargs):
        return self.get_html_from_json(fail_silently=True)


class FeedContent(models.Model):
    url = models.URLField(
        _('Feed URL'),
        help_text=_(
            'Paste here any RSS Feed URL.'
            ' F.e. https://www.djangoproject.com/rss/weblog/'),
    )

    class Meta:
        abstract = True
        verbose_name = _('RSS Feed')
        verbose_name_plural = _('RSS Feeds')

    def clean(self, *args, **kwargs):
        import feedparser
        feedparser.parse(CachedLookup.objects.request(self.url, 30 * 60))

    @property
    def feed(self):
        import feedparser
        return feedparser.parse(
            CachedLookup.objects.request(self.url, 30 * 60))

    def render(self, **kwargs):
        return render_to_string('content/external/feed.html', {
            'feed': self.feed,
        })


class OembedMixin(models.Model):
    """
    Mixin for usage in custom feincms content types
    Usage::

        Page.create_content_type(
            YourContentWithOembedMixin,
            OEMBED_PARAMS={
                'maxwidth': 500,
                'maxheight': 300,
                'wmode': 'transparent',
            },
        )

    Oembed content will be available via self.oembed
    """

    url = models.URLField(
        _('Video URL'),
        help_text=_(
            'Insert an URL to an external content you want to embed,'
            ' f.e. http://www.youtube.com/watch?v=Nd-vBFJN_2E'),
        blank=True,
    )

    class Meta:
        abstract = True

    @classmethod
    def initialize_type(cls, OEMBED_PARAMS={}):
        cls._params = OEMBED_PARAMS

    def get_html_from_json(self, fail_silently=False):
        if not self.url:
            self.oembed = ''
            return True

        params = {}
        params.update(self._params)

        try:
            embed = CachedLookup.objects.oembed(self.url, **params)
        except TypeError:
            if fail_silently:
                return u''
            raise ValidationError(
                _('I don\'t know how to embed %s.') % self.url)

        self.oembed = embed

    def process(self, request, **kwargs):
        self.get_html_from_json()
