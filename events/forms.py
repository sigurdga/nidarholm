from django.forms import ModelForm
from samklang_utils.forms import MarkdownTextarea
from events.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'location', 'start', 'end', 'whole_day', 'content', 'event_category', 'project')
        widgets = {'content': MarkdownTextarea()}
