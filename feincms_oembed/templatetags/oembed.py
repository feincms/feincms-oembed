import json

from django import template
from django.utils.http import urlquote

from feincms_oembed.models import CachedLookup


register = template.Library()


class Oembed(template.Node):
    def __init__(self, url, params):
        self.url = template.Variable(url)
        self.params = template.Variable(params)

    def render(self, context):
        try:
            url = self.url.resolve(context)

            # TODO use configured provider instead
            ooembed_url = 'http://api.embed.ly/1/oembed?url=%s&%s' % (
                urlquote(url), self.params)

            lookup, created = CachedLookup.objects.get_or_create(url=ooembed_url)

            try:
                data = json.loads(lookup.response)
                html = data.get('html')
            except ValueError:
                raise template.TemplateSyntaxError(
                    'The specified url %s does not respond oembed json' % ooembed_url)

            if html:
                return html
            elif data.get('type') == 'photo':
                # TODO: Research for different types and build templates for it
                return u'<img src="%s" />' % data.get('url')
            else:
                return u'<!-- could not parse response %s -->' % data
        except template.VariableDoesNotExist, e:
            return u'<!-- %s -->' % e


@register.tag(name='oembed')
def do_oembed(parser, token):
    # TODO KILL IT WITH FIRE
    # ... or rewrite it completely
    try:
        tag_name, url, params = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s tag requires a single argument (url) and optional params' % token.contents.split()[0]
    return Oembed(url, params)
