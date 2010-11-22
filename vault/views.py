from django.http import HttpResponseRedirect, HttpResponse, Http404
from permissions.middleware.http import Http403
from django.shortcuts import get_object_or_404, render_to_response
from vault.models import UploadedFile
from vault.forms import UploadedFileForm
from django.core.urlresolvers import reverse
#from django.core.servers.basehttp import FileWrapper
import os
from django.conf import settings
from django.views.generic import list_detail
from tagging.models import TaggedItem
from django.template.context import RequestContext
import pyexiv2
import magic

FORMAT = "jpeg"
QUALITY = 75

def new_file(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.filename = request.FILES['file'].name
            #original_filename = "{root}originals/{filename}".format(
            #    root=settings.FILE_SERVE_ROOT,
            #    filename=uploaded_file.file)
            #import pdb; pdb.set_trace()
            #uploaded_file.content_type = magic.Magic(mime=True).from_file(original_filename)
            uploaded_file.content_type = request.FILES['file'].content_type
            uploaded_file.save()
            return HttpResponseRedirect('/files')
    else:
        uploadedfile = UploadedFile()
        form = UploadedFileForm(instance=uploadedfile)
    return render_to_response('vault/new_file.html', {'form': form}, context_instance=RequestContext(request))

def file_list(request, tags=""):

    if tags:
        tags = tags.split("/")
        queryset = UploadedFile.objects.for_user(request.user)
        queryset = TaggedItem.objects.get_by_model(queryset, tags)
    else:
        tags = []
        queryset = UploadedFile.objects.for_user(request.user)

    menu_tags = [ (reverse('vault-tagged-file-list', args=[tag]), tag) for tag in tags ]

    return list_detail.object_list(request,
                                   queryset=queryset,
                                   paginate_by=20,
                                   extra_context={
                                           'tags': tags,
                                           'menu_tags': menu_tags,
                                           },
                                   )

def file_object_detail(request, id):
    return list_detail.object_detail(request,
                                     UploadedFile.objects.for_user(request.user),
                                     id,
                                     )

def send_file(request, id, size=settings.DEFAULT_IMAGE_SIZE):
    size = int(size)
    uploaded_file = get_object_or_404(UploadedFile, id=id)
    if uploaded_file.group and not uploaded_file.group in request.user.groups.all():
        raise Http403

    original_filename = settings.FILE_SERVE_ROOT + "originals/" + uploaded_file.file.name
    filetype = uploaded_file.content_type.split('/')[0]

    if filetype != "image":
        filename = original_filename
    else:
        filename = settings.FILE_SERVE_ROOT + "cache/" + uploaded_file.file.name + "/" + str(size)

        if not os.path.exists(filename):
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

            try:
                import Image
            except ImportError:
                try:
                    from PIL import Image
                except ImportError:
                    raise ImportError('Cannot import the Python Image Library.')

            image = Image.open(original_filename)
            exif = pyexiv2.Image(original_filename)
            exif.readMetadata()

            if 'Exif.Image.Orientation' in exif.exifKeys():
                orientation = exif['Exif.Image.Orientation']
                if orientation == 1:
                    # Nothing
                    pass
                elif orientation == 2:
                    # Vertical Mirror
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    # Rotation 180
                    image = image.transpose(Image.ROTATE_180)
                elif orientation == 4:
                    # Horizontal Mirror
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                elif orientation == 5:
                    # Horizontal Mirror + Rotation 270
                    image = image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
                elif orientation == 6:
                    # Rotation 270
                    image = image.transpose(Image.ROTATE_270)
                elif orientation == 7:
                    # Vertical Mirror + Rotation 270
                    image = image.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
                elif orientation == 8:
                    # Rotation 90
                    image = image.transpose(Image.ROTATE_90)

            # normalize image mode
            if image.mode != 'RGB':
                image = image.convert('RGB')

            method = "crop"
            delete_exif_thumbnail = True
            if size == 1:
                width, height = 40, 40
            elif size == 2:
                width, height = 100, 100
            elif size == 3:
                width, height = 160, 160
            elif size == 4:
                width, height = 220, 220
            elif size == 5:
                if image.size[0] > image.size[1]:
                    width, height = 280, 210
                else:
                    width, height = 210, 280
            elif size == 6:
                if image.size[0] > image.size[1]:
                    width, height = 340, 255
                else:
                    width, height = 255, 340
            elif size == 7:
                if image.size[0] > image.size[1]:
                    width, height = 400, 300
                else:
                    width, height = 300, 400
            elif size == 8:
                if image.size[0] > image.size[1]:
                    width, height = 460, 345
                else:
                    width, height = 345, 460
            elif size == 0:
                width, height = 520, 520
                method = "scale"
                delete_exif_thumbnail = False

            # use PIL methods to edit images
            if method == 'scale':
                image.thumbnail((width, height), Image.ANTIALIAS)
                image.save(filename, FORMAT, quality=QUALITY)

            elif method == 'crop':
                try:
                    import ImageOps
                except ImportError:
                    from PIL import ImageOps

                ImageOps.fit(image, (width, height), Image.ANTIALIAS).save(
                    filename, FORMAT, quality=QUALITY)

            if exif:
                if delete_exif_thumbnail:
                    exif.deleteThumbnail()

                new_file_exif = pyexiv2.Image(filename)
                new_file_exif.readMetadata()

                # reset image orientation for new image
                exif.copyMetadataTo(new_file_exif)
                new_file_exif['Exif.Image.Orientation'] = 1
                #new_file_exif['Exif.Image.XResolution'] = 11.1
                #new_file_exif['Exif.Image.YResolution'] = 1
                new_file_exif['Exif.Image.ImageWidth'] = width
                new_file_exif['Exif.Image.ImageLength'] = height

                new_file_exif.writeMetadata()

    f = open(filename, 'r')
    output = f.read()
    f.close()
    response = HttpResponse(content_type=uploaded_file.content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'filename=%s' % (uploaded_file.filename)
    response.write(output)
    return response
