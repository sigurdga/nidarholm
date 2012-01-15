from django.forms import ModelForm
from vault.models import UploadedFile
from fileupload.widgets import UploadWidget

class UploadedFileForm(ModelForm):
    class Meta:
        model = UploadedFile
        exclude = ('user', 'filename', 'content_type')
        widgets = {'file': UploadWidget(upload={'rowselector': 'div.ctrlHolder'})}
