from django.views.generic import list_detail
from organization.models import GroupCategory


def group_category_list(request):
    return list_detail.object_list(request, GroupCategory.objects.all())

def group_category_detail(request, slug, group_slug):
    return list_detail.object_detail(request, GroupCategory.objects.all(), slug=slug,
            extra_context={'group_name': group_slug})
