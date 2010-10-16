from navigation.models import Link
from django.views.generic import list_detail

def sitemap(request):
        return list_detail.object_list(request,
               queryset=Link.objects.filter(parent=None),
               template_name='navigation/sitemap.html',
               )
