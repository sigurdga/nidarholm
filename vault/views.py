from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from vault.models import UploadedFile
from vault.forms import UploadedFileForm

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
