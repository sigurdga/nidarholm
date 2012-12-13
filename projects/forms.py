from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from projects.models import Project
from django.contrib.auth.models import User

from samklang_utils.forms import MarkdownTextarea

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'content', 'group', 'tag', 'start', 'end', 'users')
        widgets = {
                'users': CheckboxSelectMultiple(),
                'content': MarkdownTextarea(),
                }

    def __init__(self, *args, **kwargs):
        def new_label_from_instance(self, obj):
            return "%s (%s)" % (obj.get_full_name(), obj.username)

        super(ProjectForm, self).__init__(*args, **kwargs)
        funcType = type(self.fields['users'].label_from_instance)
        self.fields['users'].label_from_instance = funcType(new_label_from_instance, self.fields['users'], forms.models.ModelMultipleChoiceField)
        self.fields['users'].help_text = ""
        self.fields['users'].queryset = User.objects.filter(groups__id=10).order_by("first_name")
