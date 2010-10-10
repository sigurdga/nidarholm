from django.db import models
from django.contrib.auth.models import User, Group
from tagging.models import TaggedItem
import time
from django.db.models.query_utils import Q
from tagging.fields import TagField

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
    timestamp = time.strftime('%s')
    folder = timestamp[-1]
    instance.filename = filename
    return 'files/' + folder + '/' + timestamp

class UploadedFile(models.Model):
    file = models.FileField(upload_to=upload_path)
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
        return ('file_details', (), {'id': self.id})

#tagging.register(UploadedFile)
