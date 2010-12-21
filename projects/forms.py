from django.forms import ModelForm
from projects.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'content', 'group', 'admingroup', 'tag', 'start', 'end')
