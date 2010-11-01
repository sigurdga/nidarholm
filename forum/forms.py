from django.forms import ModelForm, HiddenInput
from forum.models import Debate

class DebateForm(ModelForm):
    class Meta:
        model = Debate
        fields = ('text', 'title', 'group', 'parent')
        widgets = {
                'parent': HiddenInput(),
                }
