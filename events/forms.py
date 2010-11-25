from django.forms import ModelForm
from events.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'content', 'event_category', 'start', 'end', 'whole_day')
