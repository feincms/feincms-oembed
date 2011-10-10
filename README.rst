==============
feincms-oembed
==============

``feincms-oembed`` converts standard URLs from more than 200 content
providers into embedded videos, images and rich article previews by
letting Embedly_ to the hard work.


It's stunningly simple to use:

1. Add ``'feincms_oembed'`` to ``INSTALLED_APPS``.
2. Create the content type::

    from feincms.module.page.models import Page
    from feincms_oembed.contents import OembedContent

    Page.create_content_type(OembedContent)

3. There is no third step!


If you want to customize the Embedly_ request or use another OEmbed provider,
set ``OEMBED_PROVIDER`` to a function receiving the URL and a dict with
additional arguments and returning a suitable URL which returns OEmbed JSON
on access. ``OEMBED_PROVIDER`` must either be a dotted python path or a
callable::

    from feincms_oembed.models import oembed_provider
    def my_provider(url, kwargs):
        kwargs['wmode'] = 'opaque'
        return oembed_provider(url, kwargs)
    OEMBED_PROVIDER = my_provider


.. _Embedly: http://embed.ly/


Using the ``FeedContent``
=========================

If you want to use the ``FeedContent``, make shure you have ``feedparser`` in your Python Path:
https://code.google.com/p/feedparser/