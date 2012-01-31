# -*- encoding: utf-8 -*-

from django.views.generic import list_detail
from organization.models import GroupCategory, SiteProfile
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.utils import simplejson
from django.http import HttpResponse
from accounts.models import UserProfile


def group_category_list(request):
    return list_detail.object_list(request, GroupCategory.objects.all())

def group_category_detail(request, slug, group_slug, status_id=None):
    users_without_status = request.organization.group.user_set.filter(userprofile__status=None).order_by('-id')
    members_not_on_mailinglist = request.organization.group.user_set.filter(Q(userprofile__status=None)|Q(userprofile__status__gt=3)).order_by('-id')
    users_not_members = User.objects.filter(groups=None).order_by('-id')
    if not status_id:
        queryset = GroupCategory.objects.all()
        return list_detail.object_detail(request, queryset, slug=slug,
            extra_context={'group_name': group_slug, 'users_without_status': users_without_status, 'users_not_members': users_not_members, 'members_not_on_mailinglist': members_not_on_mailinglist})
    else:
        if request.organization.group in request.user.groups.all():
            queryset = UserProfile.objects.filter(status=status_id).select_related('user').order_by('user__first_name', 'user__last_name')
        else:
            queryset = UserProfile.objects.empty()
        return list_detail.object_list(request, queryset, template_name="organization/status.html")

def trans(string):
    string = string.replace(u"æ","a")
    string = string.replace(u"ø","o")
    string = string.replace(u"å","a")
    string = string.replace(u" ","")
    return string

from django.conf import settings
from Crypto.Cipher import AES
import base64
PADDING = '{'
BLOCK_SIZE = 32
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def email_lists_json(request, groups):
    secret = settings.SECRET_KEY[0:16]
    cipher = AES.new(secret)
    decoded = DecodeAES(cipher, groups)
    data = simplejson.loads(decoded)
    group_list = data['groups']
    prefix = data['prefix']
    organization_group = request.organization.group #SiteProfile.objects.get(site=request.site).group #site__name="Musikkforeningen Nidarholm").group
    lists = {}
    for group in group_list:
        listname = prefix + trans(group.lower())
        lists[listname] = []
        g = Group.objects.get(name=group)
        for user in g.user_set.all():
            if organization_group in user.groups.all():
                if user.get_profile().status < 4 and user.email:
                    lists[listname].append(user.email)
    return HttpResponse(content=EncodeAES(cipher, simplejson.dumps(lists)), mimetype="application/octet-stream")
