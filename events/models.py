from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from core.models import Common, Title, Markdown

class EventCategory(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('event_category_details', (), {'slug', self.slug})

    class Meta:
        verbose_name = _('Event category')
        verbose_name_plural = _('Event categories')


class Event(Common, Title, Markdown):
    #place = models.ForeignKey('Place', blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    whole_day = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    # when adding re-occurrences, use event_serie with an incremented value
    event_serie = models.IntegerField(blank=True, null=True)
    event_category = models.ForeignKey(EventCategory, blank=True, null=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('events-event', (), {
                                     'year': self.start.year,
                                     'month': self.start.month,
                                     'day': self.start.day,
                                     'slug': self.slug
                                     }
        )

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('-start',)
        get_latest_by = 'start'
