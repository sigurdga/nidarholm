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

    def __init__(self, *args, **kwargs):
        self._debates = None
        self._children_tree = None
        self._last_commentor = None
        self._last_comment_time = None
        super(Debate, self).__init__(*args, **kwargs)

    def get_thread_summary(self, key):
        latest_date, user_id = self.debates[key]
        for child in self.children_tree[key]:
            e, u= self.get_thread_summary(child)
            if d > latest_date:
                latest_date, user_id = e, u
    
        return (latest_date, user_id)
    
    def get_last_comment_time(self):
        if self._last_comment_time == None:
            self.get_forum_summaries()
            self._last_comment_time, self.last_commentor = self.get_thread_summary(self.id)
        return self._last_comment_time

    def get_last_commentor(self):
        if self._last_commentor == None:
            self.get_forum_summaries()
            self._last_comment_time, self.last_commentor = self.get_thread_summary(self.id)
        return self._last_commentor

    def get_forum_summaries(self):
        if self._debates == None:
            from django.db import connection
            cursor = connection.cursor()
        
            cursor.execute("select id, parent_id, created, user_id from forum_debate")
        
            debates = {}
            children_for_debate = {}
            for id, parent_id, created, user_id in cursor.fetchall():
                debates[id] = (created, user_id)
                children = children_for_debate.setdefault(parent_id, set())
                children.add(id)
