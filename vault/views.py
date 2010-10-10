from django.http import HttpResponseRedirect, HttpResponse
from permissions.middleware.http import Http403
from django.shortcuts import get_object_or_404, render_to_response
from vault.models import UploadedFile
from vault.forms import UploadedFileForm
#from django.core.servers.basehttp import FileWrapper
import os
from django.conf import settings
from django.views.generic import list_detail
from tagging.models import TaggedItem
from django.template.context import RequestContext

def new_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedfile = form.save(commit=False)
            uploadedfile.user = request.user
            uploadedfile.filename = request.FILES['file'].name
            uploadedfile.content_type = request.FILES['file'].content_type
            uploadedfile.save()
            return HttpResponseRedirect('/files')
    else:
        uploadedfile = UploadedFile()
        form = UploadedFileForm(instance=uploadedfile)
    return render_to_response('vault/new_file.html', {'form': form}, context_instance=RequestContext(request))

def file_list(request, tags="", page=1):
    if tags:
        tags = tags.split("/")
        queryset = UploadedFile.objects.for_user(request.user)
        queryset = TaggedItem.objects.get_by_model(queryset, tags)
    else:
        tags = []
        queryset = UploadedFile.objects.for_user(request.user)

    return list_detail.object_list(request,
                                   queryset=queryset,
                                   page=page,
                                   extra_context={'tags': tags},
                                   )

def file_object_detail(request, id):
    return list_detail.object_detail(request,
                                     UploadedFile.objects.for_user(request.user),
                                     id,
                                     )

def send_file(request, id):
    uploaded_file = get_object_or_404(UploadedFile, id=id)
    if not request.user.has_perm('view', uploaded_file):
        raise Http403
    filename = settings.MEDIA_ROOT + uploaded_file.file.name
    #import pdb; pdb.set_trace()
    #wrapper = FileWrapper(open(filename))
    f = open(filename, 'r')
    output = f.read()
    f.close()
    response = HttpResponse(content_type=uploaded_file.content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'filename=%s' % (uploaded_file.filename)
    response.write(output)
    return response
