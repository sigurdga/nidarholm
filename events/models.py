from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Common, Title, Markdown
from projects.models import Project

import datetime

class EventCategory(models.Model):
    title = models.CharField(_("title"), max_length=20)
    slug = models.SlugField()
    description = models.TextField(_("description"), blank=True)

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
    location = models.CharField(_("location"), max_length=50, blank=True, null=True)
    whole_day = models.BooleanField(_("whole day"), default=False, help_text=_("You can also check this when you do not know the time"))
    start = models.DateTimeField(_("start"), help_text=_("Set date or date and time"))
    end = models.DateTimeField(_("end"), help_text=_("Optional"), blank=True, null=True)
    # when adding re-occurrences, use event_serie with an incremented value
    event_serie = models.IntegerField(_("event serie"), blank=True, null=True)
    event_category = models.ForeignKey(EventCategory, verbose_name=_("event category"), blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name=_("project"), blank=True, null=True)

    def __unicode__(self):
        return self.title

    def in_future(self):
        return self.start > datetime.datetime.now()

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
        ordering = ('start',)
        get_latest_by = 'start'
