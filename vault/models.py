from django.db import models
from django.contrib.auth.models import User, Group
from tagging.models import TaggedItem
import time
from django.db.models.query_utils import Q
from tagging.fields import TagField
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class FileManager(models.Manager):

    def for_user(self, user):
        if user and user.is_authenticated():
            return self.get_query_set().filter(Q(group=None) | Q(group__user=user))
        else:
            return self.get_query_set().filter(group=None)

    def tagged(self, tags_string):
        tags = tags_string.split("/")
        return TaggedItem.objects.get_by_model(UploadedFile, tags)


def upload_path(instance, filename):
    # To save outside of media root, we have to make a new FileStorage,
    # where we could pass extra path info too.
    # Now using media_root, knowing we have to limit access to media/files
    timestamp = time.strftime('%s')
    folder = timestamp[-2:]
    instance.filename = filename
    return folder + '/' + timestamp


class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_path, storage=FileSystemStorage(location=settings.FILE_SERVE_ROOT + '/originals'))
    content_type = models.CharField(max_length=15, blank=True)
    filename = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, blank=True, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    tags = TagField()

    objects = FileManager()

    def __unicode__(self):
        return self.filename

    @models.permalink
    def get_absolute_url(self):
        return ('vault-file', (), {'id': self.id})

    def is_image(self):
        if self.content_type.startswith('image'):
            return True

#tagging.register(UploadedFile)
