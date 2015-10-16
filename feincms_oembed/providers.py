from django.utils.http import urlencode
from django.conf import settings


def embedly_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://embed.ly/
    Embedly requires an API key.
    """
    kwargs['url'] = url
    kwargs['key'] = settings.EMBEDLY_KEY
    return 'https://api.embed.ly/1/oembed?%s' % urlencode(kwargs)


def noembed_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://noembed.com/
    """
    kwargs['url'] = url
    return 'http://noembed.com/embed?%s' % urlencode(kwargs)
