from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

from projects.models import Project
from projects.forms import ProjectForm


def project_list(request):
    queryset = Project.objects.for_user(request.user)

    return object_list(request, queryset)

def project_detail(request, slug):
    queryset = Project.objects.for_user(request.user)

    return object_detail(request, queryset, slug=slug)

def new_project(request):
    if request.method == 'POST':
        project = Project()
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save(commit=False)
            project.user = request.user
            project.admingroup = request.organization.admingroup
            project.save()
            form.save_m2m()
            return HttpResponseRedirect(project.get_absolute_url())

    else:
        project = Project()
        form = ProjectForm(instance=project)
    return render_to_response('projects/new_project.html', {'form': form}, context_instance=RequestContext(request))

def edit_project(request, slug):
    if request.method == 'POST':
        project = get_object_or_404(Project, slug=slug)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(project.get_absolute_url())

    else:
        project = get_object_or_404(Project, slug=slug)
        form = ProjectForm(instance=project)
    return render_to_response('projects/new_project.html', {'form': form}, context_instance=RequestContext(request))
