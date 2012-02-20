from django.forms import ModelForm, HiddenInput
from samklang_utils.forms import MarkdownTextarea, AutoupdateTextInput
from news.models import Story

class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'content', 'group', 'parent')
        widgets = {
                'parent': HiddenInput(),
                'content': MarkdownTextarea(),
                'title': AutoupdateTextInput(),
                }
