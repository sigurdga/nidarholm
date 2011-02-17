from django.views.generic import list_detail
from organization.models import GroupCategory
from django.contrib.auth.models import User
from django.db.models import Q
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
