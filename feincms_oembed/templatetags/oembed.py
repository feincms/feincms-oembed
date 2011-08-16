from django import template
from django.utils import simplejson
from django.utils.http import urlquote

from feincms_oembed.models import LookupCached


register = template.Library()


class Oembed(template.Node):
    def __init__(self, url, params):
        self.url = template.Variable(url)
        self.params = template.Variable(params)

    def render(self, context):
        try:
            url = self.url.resolve(context)

            oohembed_url = 'http://api.embed.ly/1/oembed?url=%s&%s' % (urlquote(url), self.params)

            lookup, created = LookupCached.objects.get_or_create(url=oohembed_url)

            try:
                json = simplejson.loads(lookup.response)
                html = json.get('html')
            except simplejson.JSONDecodeError:
                raise template.TemplateSyntaxError('The specified url %s does not respond oembed json' % oohembed_url)

            if html:
                return html
            elif json.get('type') == 'photo':
                # TODO: Research for different types and build templates for it
                return u'<img src="%s" />' % json.get('url')
            else:
                return u'<!-- could not parse response %s -->' % json
        except template.VariableDoesNotExist, e:
            return u'<!-- %s -->' % e

@register.tag(name='oembed')
def do_oembed(parser, token):
    try:
        tag_name, url, params = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, '%s tag requires a single argument (url) and optional params' % token.contents.split()[0]
    return Oembed(url, params)