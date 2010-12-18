from django.views.generic.list_detail import object_list, object_detail

from projects.models import Project


def project_list(request):
    queryset = Project.objects.for_user(request.user)

    return object_list(request, queryset)

def project_detail(request, slug):
    queryset = Project.objects.for_user(request.user)
    
    return object_detail(request, queryset, slug=slug)


