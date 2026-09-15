import json

from django.test import SimpleTestCase, tag

from feincms_oembed.models import CachedLookup

from .test_admin import VIDEO


@tag("live")
class LiveProviderTestCase(SimpleTestCase):
    """
    Actually talks to the configured oEmbed provider.

    Excluded from the standard test run (the provider is flaky enough to turn
    unrelated pull requests red). The "Live provider" job runs it once per
    workflow run so we still notice when the service goes away for good.
    """

    def test_provider_returns_oembed_data(self):
        url = CachedLookup.objects.oembed_provider(VIDEO, {})

        lookup = CachedLookup(url=url)
        lookup.clean()

        response = json.loads(lookup._response)

        self.assertNotIn("error", response)
        self.assertEqual(response["type"], "video")
        self.assertIn("youtube.com/embed/", response["html"])
