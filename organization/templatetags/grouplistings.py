from django import template
from django.contrib.auth.models import Group
from organization.models import GroupCategory, Role

import re

register = template.Library()

def roles_for_user_in_group(user, group):
    return Role.objects.filter(membership__user=user, membership__group=group)

def phone_number_format(number):
    if number:
        m = re.search(r'^((?:4|9)\d{2})(\d{2})(\d{3})$', number)
        if m:
            return "%s %s %s" % (m.group(1), m.group(2), m.group(3))
        else:
            n = re.search(r'^(\d{2})(\d{2})(\d{2})(\d{2})$', number)
            if n:
                return "%s %s %s %s" % (n.group(1), n.group(2), n.group(3), n.group(4))
            else:
                return number
    

@register.simple_tag
def list_groups(request, group_name, groupcategory_name):
    """Give a group and a not related group category.
    Lists all groups in groupcategory, filtered on users in the given group.
    """

    group = Group.objects.get(name__iexact=group_name)
    groupcategory = GroupCategory.objects.get(name=groupcategory_name)

    #TODO: Add 404 on exceptions
    ret = "<ul>"
    for groupprofile in groupcategory.groupprofile_set.all():
        ret += "<li>"
        ret += "<h2>" + groupprofile.group.name + "</h2>"
        ret += "<table>"
        for u in groupprofile.group.user_set.all():
            # groupprofile.group.user_set.filter(groups=group) is too eager
            #if u.groups.filter(id=group.id).exists():
            if u.userprofile_set.filter(status__lt=4):
                ret += "<tr>"
                if request.organization.group in request.user.groups.all():
                    ret += "<td class=\"col4\"><a href=\"" + u.get_absolute_url() +"\">" + u.get_full_name() + "</a></td>"
                else:
                    ret += "<td class=\"col4\">" + u.get_full_name() + "</td>"
                ret += "<td>" + ", ".join([ role.name for role in roles_for_user_in_group(u, group) ]) + "</td>"
                if request.user.groups.filter(id=group.id):
                    ret += "<td class=\"col2\">%s</td>" % (phone_number_format(u.get_profile().cellphone) or "",)
                    ret += "<td class=\"col5\">%s</td>" % (u.email,)
                ret += "<td>" + ", ".join([ role.name for role in roles_for_user_in_group(u, groupprofile.group) ]) + "</td>"
                ret += "</tr>"
        ret += "</table>"
        ret += "</li>"
    ret += "</ul>"
    return ret
