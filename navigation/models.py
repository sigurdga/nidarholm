from django.db import models
from django.utils.translation import ugettext_lazy as _

class Link(models.Model):
    title = models.CharField(_('title'), max_length=30)
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    parent = models.ForeignKey('Link', null=True, blank=True, related_name='children')
    older_sibling = models.ForeignKey('Link', null=True, blank=True, related_name='younger_siblings')
    
    def __unicode__(self):
        return self.title + ": " + self.url