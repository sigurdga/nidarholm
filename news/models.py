from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from pages.models import extend_markdown
#from django.contrib.contenttypes import generic
from django.db.models.query_utils import Q

class NewsManager(models.Manager):
    
    def for_user(self, user):
        if user.is_authenticated():
            return self.get_query_set().filter(Q(group=None)|Q(group__user=user))
        else:
            return self.get_query_set().filter(group=None)

class Story(models.Model):
    parent = models.ForeignKey('Story', null=True, blank=True, related_name='children')
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField(_('HTML content'), blank=True)
    content_markdown = models.TextField(_('content'), blank=True, help_text=_('Use Markdown syntax'))
    pub_date = models.DateTimeField(auto_now_add=True)
    #permissions = generic.GenericRelation(ObjectPermission)
    group = models.ForeignKey(Group, blank=True, null=True)
    
    objects = NewsManager()
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news-story', (), {
                              'slug': self.slug,
                              'year': self.pub_date.year,
                              'month': self.pub_date.month,
                              'day': self.pub_date.day,
                              }
        )

    def save(self):
        self.content = extend_markdown(self.content_markdown)
        super(Story, self).save()
