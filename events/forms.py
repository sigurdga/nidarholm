from django.forms import ModelForm
from events.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('user', 'text_html', 'slug', 'event_serie')
