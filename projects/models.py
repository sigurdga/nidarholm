from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag
from core.models import Common, Title, Markdown

class Project(Common, Title, Markdown):
    start = models.DateTimeField(verbose_name=_('project start'))
    end = models.DateTimeField(verbose_name=_('project end'))
    tag = models.ForeignKey(Tag, null=True, blank=True,
            verbose_name=_('project tag'))
    users = models.ManyToManyField(User, null=True, blank=True,
            related_name='user_of_projects',
            verbose_name = _('project group'))
    admingroup = models.ForeignKey(Group, related_name='administers_projects',
            verbose_name = _('administration group'), blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ('-end',)
