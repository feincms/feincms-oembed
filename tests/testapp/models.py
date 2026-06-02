from feincms.module.page.models import Page

from feincms_oembed.contents import OembedContent


Page.register_templates(
    {
        "key": "base",
        "title": "Base Template",
        "path": "base.html",
        "regions": [("main", "Main region")],
    }
)
Page.create_content_type(
    OembedContent, TYPE_CHOICES=[("default", "Default presentation", {})]
)
