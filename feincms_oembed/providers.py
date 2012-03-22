from django.utils.http import urlencode


def embedly_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://embed.ly/
    """
    kwargs['url'] = url
    return 'http://api.embed.ly/1/oembed?%s' % urlencode(kwargs)


def noembed_oembed_provider(url, kwargs):
    """
    Provider for the oEmbed service at http://noembed.com/
    """
    kwargs['url'] = url
    return 'http://noembed.com/embed?%s' % urlencode(kwargs)
