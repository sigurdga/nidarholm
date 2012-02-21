from django.forms import ModelForm
from samklang_utils.forms import MarkdownTextarea
from events.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'content', 'event_category', 'start', 'end', 'whole_day')
        widgets = {'content': MarkdownTextarea()}
