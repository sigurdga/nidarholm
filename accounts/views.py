from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from django.contrib.auth.models import User, Group
from accounts.forms import UserGroupsForm
from django.template.context import RequestContext

def groups(request):
        return list_detail.object_list(request, Group.objects.all(), template_name="accounts/group_list.html")

def group_object_detail(request, id):
    return list_detail.object_detail(request, Group.objects.all(), object_id=id, template_name="accounts/group_detail.html")

def user_groups(request, username):
    user = User.objects.get(username=username)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserGroupsForm(request.POST)
            if form.is_valid():
                user.groups = form.cleaned_data['groups']
                return HttpResponseRedirect("")
        else:
            groups = []
            for group in user.groups.all():
                groups.append(group.id)

            form = UserGroupsForm(initial={'id': user.id, 'groups': groups})
        return list_detail.object_list(request, Group.objects.all(), extra_context={'this_user': user, 'form': form}, template_name="accounts/edit_user_groups.html")
    else:
        return list_detail.object_list(request, user.groups.all(), extra_context={'this_user': user}, template_name="accounts/user_groups.html")

def member_list(request):
    members = User.objects.filter(groups=request.organization.group).order_by('first_name, last_name')
    user_ok = request.organization.group in request.user.groups.all()
    return list_detail.object_list(request, members, template_name="accounts/members.html", extra_context={'user_ok': user_ok})
