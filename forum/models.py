from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from core.models import Common, Title, Markdown

class Debate(Common, Title, Markdown):
    _debates = None
    _children_for_debate = None
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
        self._last_commentor = None
        self._last_comment_time = None
        self._comment_count = None
        super(Debate, self).__init__(*args, **kwargs)

    def get_thread_summary(self, key):
        latest_date, user_id = Debate._debates[key]
        count = 1
        
        try:
            for child in Debate._children_for_debate[key]:
                d, u, c = self.get_thread_summary(child)
                count += c
                if d > latest_date:
                    latest_date, user_id = d, u
        except KeyError:
            pass
    
        return latest_date, user_id, count
    
    def get_last_comment_time(self):
        if self._last_comment_time == None:
            self.get_forum_summaries()
            self._last_comment_time, last_commentor, comment_count = self.get_thread_summary(self.id)
            self._comment_count = comment_count - 1
            self._last_commentor = User.objects.get(pk=last_commentor)
        return self._last_comment_time

    def get_last_commentor(self):
        if self._last_commentor == None:
            self.get_forum_summaries()
            self._last_comment_time, last_commentor, comment_count = self.get_thread_summary(self.id)
            self._comment_count = comment_count - 1
            self._last_commentor = User.objects.get(pk=last_commentor)
        return self._last_commentor

    def get_comment_count(self):
        if self._comment_count == None:
            self.get_forum_summaries()
            self._last_comment_time, last_commentor, comment_count = self.get_thread_summary(self.id)
            self._comment_count = comment_count - 1
            self._last_commentor = User.objects.get(pk=last_commentor)
        return self._comment_count

    def get_forum_summaries(self):
        if Debate._debates == None:
            from django.db import connection
            cursor = connection.cursor()
        
            cursor.execute("select id, parent_id, created, user_id from forum_debate")
        
            Debate._debates = {}
            Debate._children_for_debate = {}
            for id, parent_id, created, user_id in cursor.fetchall():
                Debate._debates[id] = (created, user_id)
                children = Debate._children_for_debate.setdefault(parent_id, set())
                children.add(id)
