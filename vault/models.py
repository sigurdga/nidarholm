from django.db import models
from django.contrib.auth.models import User
import tagging
import time

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
    uploaded = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.filename
    
    @models.permalink
    def get_absolute_url(self):
        return ('file_details', (), {'id': self.id})

tagging.register(UploadedFile)