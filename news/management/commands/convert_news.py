from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from core.models import comment_converter
from news.models import Story
from vault.models import UploadedFile
from django.conf import settings
from s7n.threaded_comments import ThreadedComment

from datetime import datetime

import MySQLdb
import re

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):

        for story in Story.objects.filter(parent=None):
            self.make_children(story, story)

    def make_children(self, parent_story, top_story, parent_comment=None):
        for story in Story.objects.filter(parent=parent_story):
            comment = ThreadedComment()
            comment.content_object = top_story
            if parent_comment:
                comment.parent = parent_comment
            comment.user = story.user
            comment.submit_date = story.created
            comment.update_date = story.updated
            comment.content = story.content
            comment.site_id = 1
            if not comment.content:
                comment.content = "BLANK"
            comment.save()
            print "  " * comment.level,
            print comment.user
            self.make_children(story, top_story, comment)

