from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import Common, Title, Markdown

class Debate(Common, Title, Markdown):
    parent = models.ForeignKey('Debate', null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('created',)
        verbose_name = _('forum post')
        verbose_name_plural = _('forum posts')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('forum-debate', (), {'slug': self.slug})

    def get_top_url(self):
        parent = self.parent
        top = self
        while parent:
            top = parent
            parent = top.parent
        return top.get_absolute_url()
