from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Common, Title, Markdown

class Story(Common, Title, Markdown):
    parent = models.ForeignKey('Story', null=True, blank=True, related_name='children')
    pub_date = models.DateTimeField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("pub_date",)
        verbose_name  = _('news story')
        verbose_name_plural = _('news stories')

    @models.permalink
    def get_absolute_url(self):
        return ('news-story', (), {
                              'slug': self.slug,
                              'year': self.pub_date.year,
                              'month': self.pub_date.month,
                              'day': self.pub_date.day,
                              }
        )
