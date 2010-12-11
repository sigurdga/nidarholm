from django.contrib import admin
from events.models import Event, EventCategory

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'location', 'content', 'start', 'end', 'whole_day', 'user', 'group', 'event_serie', 'event_category')
    list_display = ('title', 'start', 'end', 'location', 'group')
    list_filter = ('group', 'start')
    ordering = ('-created',)
    search_fields = ('title', 'content_html')

admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory)
