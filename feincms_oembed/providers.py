from django.conf import settings
from django.utils.http import urlencode


def embedly_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://embed.ly/
    Embedly requires an API key.
    """
    kwargs["url"] = url
    kwargs["key"] = settings.EMBEDLY_KEY
    return f"https://api.embed.ly/1/oembed?{urlencode(kwargs)}"


def noembed_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://noembed.com/
    """
    kwargs["url"] = url
    return f"http://noembed.com/embed?{urlencode(kwargs)}"
