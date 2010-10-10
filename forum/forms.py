from django.forms import ModelForm, HiddenInput
from forum.models import Debate

class DebateForm(ModelForm):
    class Meta:
        model = Debate
        exclude = ('user', 'group', 'slug', 'text_html')
        widgets = {
                'parent': HiddenInput(),
                }
