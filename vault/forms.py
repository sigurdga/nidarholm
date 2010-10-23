from django.forms import ModelForm
from vault.models import UploadedFile

class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        exclude = ('user', 'filename', 'content_type')
