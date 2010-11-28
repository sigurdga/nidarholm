# -*- encoding: utf-8 -*-

from django import template
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def markdown_help():
    return """
<h1>%s</h1>

<p>%s</p>

<p>%s</p>

<p>%s</p>

<p><a href="http://daringfireball.net/projects/markdown/syntax">%s</a></p>
""" % (
        _("Syntax help"),
        _("Markdown helps you write text on the web. For bullet lists, start the lines with dash (-), plus (+) or asterisk (*) followed by space. To emphasize words, enclose them in <code>_underscores_</code> or <code>*asterisks*</code>. Two makes the emphasis <code>__stronger__</code>."),
        _("Readable links are a bit more complex, here is an example: <code>[Link text descibing the link](http://address.to/location)</code>. You can also make simpler not so readable links like this: <code>&lt;http://address.to/location&gt;</code>."),
        _("Images are similar, but you need an exclamation mark: <code>![Image description](http://address.to/picture.jpg)</code>. Use internal images like this: <code>![Image description][8]</code>. You only need the image number in brackets, but you can optinally specify the image size like: <code>![Description][8/4]</code>."),
        _("See the complete specification of the Markdown syntax"),
        )
