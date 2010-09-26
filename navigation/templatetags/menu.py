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

def html_menu(menu, active):
    return "<ul>" + "".join([ "<li>" + html_item(item, active) + "</li>" for item in menu ]) + "</ul>"    

def html_item(item, active):
    if item in active:
        return '<a href="%s" class="active">%s</a>' % (item.url, item.title)
    else:
        return '<a href="%s">%s</a>' % (item.url, item.title)
    
@register.tag
def full_menu(parser, token):
    try:
        tag_name, = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag takes only one argument" % token.contents.split()[0]
    return MenuNode()

class MenuNode(template.Node):
    def render(self, context):
        parents = []
        if 'path_info' in context:
            pages = Link.objects.filter(url=context['path_info'])
            if pages:
                page = pages[0]
                while page:
                    parents.append(page)
                    page = page.parent
        parents.append(None)
        parents.reverse()
        
        return "".join([ html_menu(make_menu(parent), parents) for parent in parents ])