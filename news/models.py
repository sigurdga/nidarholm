from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import Common, Title, Markdown

class Story(Common, Title, Markdown):
    parent = models.ForeignKey('Story', null=True, blank=True, related_name='children')
    pub_date = models.DateTimeField(verbose_name=_('publish date'), auto_now_add=True)

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

    def object_template(self):
        return "news/story.html"

    def get_top(self):
        parent = self.parent
        top = self
        while parent:
            top = parent
            parent = top.parent
        return top

