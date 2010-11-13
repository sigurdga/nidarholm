from django import template
from navigation.models import Link
from collections import deque

register = template.Library()

def make_menu(parent, user):
    menu = []
    nexts = deque(Link.objects.filter(parent=parent, older_sibling=None))
    while nexts:
        next = nexts.popleft()
        if not next.group or next.group in user.groups.all():
            menu.append(next)
        nexts.extend(next.younger_siblings.all())
    return menu

def html_menu(menu):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (item.url, item.title) for item in menu ]) + "</ul>"

def make_breadcrumbs(parents):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (parent.url, parent.title) for parent in parents ]) + "</ul>"

def make_extra_breadcrumbs(tuples):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (t[0], t[1]) for t in tuples ]) + "</ul>"


@register.simple_tag
def local_menu(request_path_info, request_user):
    try:
        page = Link.objects.get(url=request_path_info)
    except Link.DoesNotExist:
        page = Link.objects.get(url='/')
    return html_menu(make_menu(page, request_user))

@register.simple_tag
def breadcrumbs(request_path_info, request_user, extra=[]):
    parents = []
    try:
        link = Link.objects.get(url=request_path_info)
    except Link.DoesNotExist:
        link = Link.objects.get(url='/')
    if not link.group or link.group in request_user.groups.all():
        while link:
            parents.append(link)
            link = link.parent
        parents.reverse()

    return "<ul>%s%s</ul>" % (
            "".join([ '<li><a href="%s">%s</a></li>' % (parent.url, parent.title) for parent in parents ]),
            "".join([ '<li><a href="%s">%s</a></li>' % (t[0], t[1]) for t in extra ]),
            )
