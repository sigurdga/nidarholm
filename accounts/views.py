from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import list_detail
from django.contrib.auth.models import User, Group
from accounts.forms import UserGroupsForm
from django.template.context import RequestContext

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm(request)

    return render_to_response("accounts/login.html", {'form': form}, context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password1"))
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response("accounts/register.html", {'form': form})

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
