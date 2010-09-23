from django.forms import ModelForm
from vault.models import UploadedFile
from tagging.forms import TagField

class UploadedFileForm(ModelForm):
    tags = TagField()
    class Meta:
        model = UploadedFile
        exclude = ('user', 'filename', 'content_type')