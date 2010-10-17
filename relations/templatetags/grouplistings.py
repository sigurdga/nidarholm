from django import template
from django.contrib.auth.models import Group
from relations.models import GroupCategory, Role

register = template.Library()

def roles_for_user_in_group(user, group):
    return Role.objects.filter(membership__user=user, membership__group=group)

@register.simple_tag
def list_groups(request, group_name, groupcategory_name):
    """Give a group and a not related group category.
    Lists all groups in groupcategory, filtered on users in the given group.
    """

    group = Group.objects.get(name=group_name)
    groupcategory = GroupCategory.objects.get(name=groupcategory_name)

    ret = "<ul>"
    for groupprofile in groupcategory.groupprofile_set.all():
        ret += "<li>"
        ret += "<h2>" + groupprofile.group.name + "</h2>"
        ret += "<table>"
        for user in groupprofile.group.user_set.all():
            # groupprofile.group.user_set.filter(groups=group) is too eager
            if user.groups.filter(id=group.id).exists():
                ret += "<tr><td>" + user.get_full_name() + "</td>"
                ret += "<td>" + ", ".join([ role.name for role in roles_for_user_in_group(user, group) ]) + "</td>"
                if request.user.groups.filter(id=group.id):
                    ret += "<td>" + user.get_profile().cellphone + "</td>"
                ret += "<td>" + ", ".join([ role.name for role in roles_for_user_in_group(user, groupprofile.group) ]) + "</td>"
                ret += "</tr>"
        ret += "</table>"
        ret += "</li>"
    ret += "</ul>"
    return ret
