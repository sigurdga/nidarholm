from django.db import models
from django.contrib.auth.models import User, Group

class Debate(models.Model):
    parent = models.ForeignKey('Debate', null=True, blank=True, related_name='children')
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('forum_debate', (), {'slug': self.slug})
