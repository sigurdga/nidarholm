from django import template
from navigation.models import Link
from collections import deque

register = template.Library()

def make_menu(parent):
    menu = []
    nexts = deque(Link.objects.filter(parent=parent, older_sibling=None))
    while nexts:
        next = nexts.popleft()
        menu.append(next)
        nexts.extend(next.younger_siblings.all())
    return menu

def html_menu(menu):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (item.url, item.title) for item in menu ]) + "</ul>"

def make_breadcrumb(parents):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (parent.url, parent.title) for parent in parents ]) + "</ul>"


@register.simple_tag
def local_menu(request):
    try:
        page = Link.objects.get(url=request.path_info)
    except Link.DoesNotExist:
        return ""
    else:
        return html_menu(make_menu(page))

@register.simple_tag
def breadcrumbs(request):
    parents = []
    try:
        page = Link.objects.get(url=request.path_info)
    except Link.DoesNotExist:
        return ""
    else:
        while page:
            parents.append(page)
            page = page.parent
        parents.reverse()
        return make_breadcrumb(parents)
