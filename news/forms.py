from django.forms import ModelForm, HiddenInput
from news.models import Story

class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = ('content', 'title', 'group', 'parent')
        widgets = {
                'parent': HiddenInput(),
                }
