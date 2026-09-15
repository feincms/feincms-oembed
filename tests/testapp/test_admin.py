import json
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from feincms.module.page.models import Page

from feincms_oembed.models import CachedLookup


VIDEO = "https://www.youtube.com/watch?v=o6rd6i6L45Y"

# Captured from noembed.com. The service answers with an error payload every
# now and then, so the lookup is mocked instead of hitting the network.
OEMBED_RESPONSE = {
    "thumbnail_width": 480,
    "title": "Hexen - Cleric (Cardinal) 100% Speedrun in 1:37:02",
    "type": "video",
    "provider_name": "YouTube",
    "author_name": "Zero Master",
    "author_url": "https://www.youtube.com/@ZeroMaster",
    "url": VIDEO,
    "thumbnail_url": "https://i.ytimg.com/vi/o6rd6i6L45Y/hqdefault.jpg",
    "thumbnail_height": 360,
    "version": "1.0",
    "provider_url": "https://www.youtube.com/",
    "html": (
        '<iframe width="200" height="113"'
        ' src="https://www.youtube.com/embed/o6rd6i6L45Y?feature=oembed"'
        ' frameborder="0" allowfullscreen></iframe>'
    ),
    "width": 200,
    "height": 113,
}


class FakeResponse:
    def read(self):
        return json.dumps(OEMBED_RESPONSE).encode("utf-8")

    def getcode(self):
        return 200


def fake_urlopen(url):
    return FakeResponse()


class AdminTestCase(TestCase):
    @mock.patch("feincms_oembed.models.urlopen", fake_urlopen)
    def test_admin(self):
        author = User.objects.create_superuser("admin", "admin@example.com", "password")
        self.client.force_login(author)

        response = self.client.post(
            "/admin/page/page/add/",
            {
                "title": "First page",
                "slug": "first-page",
                "parent": "",
                "template_key": "base",
                "oembedcontent_set-TOTAL_FORMS": 1,
                "oembedcontent_set-INITIAL_FORMS": 0,
                "oembedcontent_set-MAX_NUM_FORMS": 1000,
                "oembedcontent_set-0-parent": "",
                "oembedcontent_set-0-url": VIDEO,
                "oembedcontent_set-0-region": "main",
                "oembedcontent_set-0-ordering": 0,
                "oembedcontent_set-0-type": "default",
            },
        )

        self.assertRedirects(
            response,
            "/admin/page/page/",
        )

        page = Page.objects.get()
        self.assertEqual(page.oembedcontent_set.count(), 1)

        lookup = CachedLookup.objects.get()
        self.assertTrue("Zero Master" in lookup._response)
