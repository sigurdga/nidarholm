from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from forum.models import Debate
from s7n.forum.models import Forum
from s7n.threaded_comments import ThreadedComment
from mptt.managers import TreeManager

from core.models import comment_converter

import MySQLdb
import time
import re
from datetime import datetime

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        for debate in Debate.objects.filter(parent=None):
            #forum = Forum.objects.get_or_create(user=debate.user, created_date=debate.created, updated_date=debate.updated)
            forum = Forum()
            forum.user = debate.user
            forum.group = debate.group
            forum.created_date = debate.created
            forum.updated_date = debate.updated
            forum.content = debate.content
            if not forum.content:
                forum.content = "BLANK"
            forum.title = debate.title
            if not forum.title:
                forum.title = "BLANK"
            forum.save()
            print forum.title
            print "----------"
            self.make_children(debate, forum)
            print ""
            print ""
        print "Rebuilding"
        ThreadedComment.tree.rebuild()

    def make_children(self, parent_debate, forum_top, parent_comment=None):
        for debate in Debate.objects.filter(parent=parent_debate):
            #comment = ThreadedComment.objects.get_or_create(user=debate.user, submit_date=debate.created, update_date=debate.updated, defaults={'content_type_id': 1, 'site_id': 1})
            comment = ThreadedComment()
            comment.content_object = forum_top
            if parent_comment:
                comment.parent = parent_comment
            comment.user = debate.user
            comment.submit_date = debate.created
            comment.update_date = debate.updated
            comment.content = debate.content
            comment.site_id = 1
            if not comment.content:
                comment.content = "BLANK"
            comment.save()
            print "  " * comment.level,
            print comment.user
            self.make_children(debate, forum_top, comment)
