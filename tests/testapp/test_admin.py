from django.contrib.auth.models import User
from django.test import TestCase
from feincms.module.page.models import Page

from feincms_oembed.models import CachedLookup


ASTLEY = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class AdminTestCase(TestCase):
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
                "oembedcontent_set-0-url": ASTLEY,
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
        self.assertTrue("Astley" in lookup._response)
