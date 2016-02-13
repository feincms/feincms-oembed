==============
feincms-oembed
==============

``feincms-oembed`` converts standard URLs from more than 200 content
providers into embedded videos, images and rich article previews by
letting Embedly_ or another OEmbed provider to the hard work.


It's stunningly simple to use:

1. Add ``'feincms_oembed'`` to ``INSTALLED_APPS``.
2. Create the content type::

    from feincms.module.page.models import Page
    from feincms_oembed.contents import OembedContent

    TYPE_CHOICES = [
        ('default', _('Default presentation'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'opaque'}),
        ('transparent', _('Transparent'), {
            'maxwidth': 500, 'maxheight': 300, 'wmode': 'transparent'}),
        ]

    Page.create_content_type(OembedContent, TYPE_CHOICES=TYPE_CHOICES)


You can also specify additional parameters which are sent to the OEmbed
provider too::

    Page.create_content_type(OembedContent, TYPE_CHOICES=TYPE_CHOICES,
        PARAMS={'wmode': 'opaque'})


By default feincms_oembed uses the Embedly_ Oembed Provider. This provider
requires an API key even for the free plan. ``settings.EMBEDLY_KEY`` must
therefore be set.
The free plan is good for 5000 URLs per month.

If you want to customize the Embedly_ request or use another OEmbed provider,
set ``settings.OEMBED_PROVIDER`` to a function receiving the URL and a dict
with additional arguments and returning a suitable URL which returns OEmbed
JSON on access. ``OEMBED_PROVIDER`` must either be a dotted python path or a
callable::

    from feincms_oembed.providers import embedly_oembed_provider
    def my_provider(url, kwargs):
        kwargs['wmode'] = 'opaque'
        return embedly_oembed_provider(url, kwargs)

    OEMBED_PROVIDER = 'path.to.module.my_provider'
    # OEMBED_PROVIDER = my_provider # The function can be used too, not only
                                    # the dotted python path.


The content is looking for templates in the following order in the folder
``content/external/``:

 1. type of the embedded object (e.g. 'video') + ``.html``
 2. type of the content type (e.g. 'transparent') + ``.html``
 3. ``default.html``

If you don't want any surprises with blocked access to Embedly_ it is suggested
that you register_ for a free API key.


Using the ``FeedContent``
=========================

If you want to use the ``FeedContent``, make sure you have feedparser_ in
your Python path.


.. _Embedly: https://embed.ly/
.. _register: https://app.embed.ly/pricing/free
.. _feedparser: https://code.google.com/p/feedparser/
