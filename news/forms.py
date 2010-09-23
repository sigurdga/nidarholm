from django.forms import ModelForm, HiddenInput
from news.models import Story

class StoryForm(ModelForm):
    class Meta:
        model = Story
        exclude = ('user', 'group', 'slug')
        widgets = {
                'parent': HiddenInput(),
                }