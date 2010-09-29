from django.http import HttpResponseRedirect, HttpResponse
from permissions.middleware.http import Http403
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from vault.models import UploadedFile
from vault.forms import UploadedFileForm
from django.core.servers.basehttp import FileWrapper
import os
from django.conf import settings

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
    return render_to_response('vault/new_file.html', {'form': form})

def file_list(request):
    file_list = UploadedFile.objects.all()
    paginator = Paginator(file_list, 25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        file_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        file_page = paginator.page(paginator.num_pages)

    return render_to_response('vault/list.html', {'files': file_page})

def file_details(request, id):
    uploaded_file = get_object_or_404(UploadedFile, id=id)
    return render_to_response('vault/file.html', {'uploaded_file': uploaded_file})

def send_file(request, id):
    uploaded_file = get_object_or_404(UploadedFile, id=id)
    if not request.user.has_perm('view', uploaded_file):
        raise Http403
    filename = settings.MEDIA_ROOT + uploaded_file.file.name
    #import pdb; pdb.set_trace()
    #wrapper = FileWrapper(open(filename))
    f = open(filename,'r')
    output = f.read()
    f.close()
    response = HttpResponse(content_type=uploaded_file.content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'filename=%s' % (uploaded_file.filename)
    response.write(output)
    return response
