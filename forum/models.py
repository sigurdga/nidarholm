from django.db import models
from core.models import TextEntry

class Debate(TextEntry):
    parent = models.ForeignKey('Debate', null=True, blank=True, related_name='children')

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
