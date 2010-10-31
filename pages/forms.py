from django.forms import ModelForm
from pages.models import FlatPage

class PageForm(ModelForm):
    class Meta:
        model = FlatPage
        exclude = ('text_html')
