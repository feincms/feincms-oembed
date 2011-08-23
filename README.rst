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

.. _Embedly: http://embed.ly/
