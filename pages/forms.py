from django.forms import ModelForm
from pages.models import FlatPage

class PageForm(ModelForm):
    class Meta:
        model = FlatPage
        exclude = ('html_content')
