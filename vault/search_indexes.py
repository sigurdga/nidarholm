import datetime
from haystack.indexes import *
from haystack import site
from vault.models import UploadedFile


class UploadedFileIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    user = CharField(model_attr='user')
    group = DateTimeField(model_attr='group', null=True)

    #def get_queryset(self):
    #    """Used when the entire index for model is updated."""
    #    return Note.objects.filter(pub_date__lte=datetime.datetime.now())


site.register(UploadedFile, UploadedFileIndex)
