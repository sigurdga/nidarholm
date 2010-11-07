from django.contrib import admin
from events.models import Event, EventCategory

admin.site.register(Event)
admin.site.register(EventCategory)
