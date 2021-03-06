from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.contrib.auth.models import User, Group
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from profiles.utils import get_profile_form

from accounts.models import UserProfile
from accounts.forms import UserGroupsForm
from accounts.forms import ProfileForm

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
    members = User.objects.filter(groups=request.organization.group).order_by('first_name', 'last_name')
    user_ok = request.organization.group in request.user.groups.all()
    return list_detail.object_list(request, members, template_name="accounts/members.html", extra_context={'user_ok': user_ok})

@login_required
def edit_profile(request, id):

    user = get_object_or_404(User, id=id)
    profile = user.get_profile()

    if request.user.is_superuser:
        form_class = get_profile_form()
    elif request.user == user:
        form_class = ProfileForm
    else:
        return HttpResponseRedirect(user.get_absolute_url())

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(user.get_absolute_url())
    else:
        form = form_class(instance=profile)

    return render_to_response('profiles/edit_profile.html',
                              { 'form': form,
                                'profile': profile, },
                              context_instance=RequestContext(request))

@login_required
def new_profile(request):

    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('member-list'))

    profile = UserProfile()
    profile.user = User()
    form_class = ProfileForm

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(profile.user.get_absolute_url())
    else:
        form = form_class(instance=profile)

    return render_to_response('profiles/edit_profile.html',
            {
                'form': form,
                'profile': profile,
                },
            context_instance=RequestContext(request))

def all_members(request):
    if request.user.is_superuser:
        members = User.objects.filter(groups=request.organization.group).order_by('first_name', 'last_name')
        return list_detail.object_list(request, members, template_name="accounts/all_about_all.html")
    else:
        raise Http404
