from django.forms import ModelForm, HiddenInput
from samklang_utils.forms import MarkdownTextarea, AutoupdateTextInput
from forum.models import Debate

class DebateForm(ModelForm):
    class Meta:
        model = Debate
        fields = ('title', 'content', 'group', 'parent')
        widgets = {
                'parent': HiddenInput(),
                'content': MarkdownTextarea(),
                'title': AutoupdateTextInput(),
                }
