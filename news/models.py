from django.db import models
from django.contrib.auth.models import User, Group

class Story(models.Model):
    parent = models.ForeignKey('Story', null=True, blank=True, related_name='children')
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    content = models.TextField()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news_story', (), {'slug': self.slug})
