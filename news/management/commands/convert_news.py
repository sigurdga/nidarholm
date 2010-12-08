from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from core.models import comment_converter
from news.models import Story
from vault.models import UploadedFile
from django.conf import settings

from datetime import datetime

import MySQLdb

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cursor.execute("select debateid, ownerid, groupid, created, title, contents, navn, brukernavn from debate inner join passord on passord.medlemid=debate.ownerid inner join gruppe on gruppe.id = debate.groupid where parentid = 155")
        for row in cursor.fetchall():
            #self.stdout.write("%s\n" % (row[4],))
            text = comment_converter(row[5])

            u = User.objects.get(username=row[7].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[6].decode('utf-8').capitalize())
            if g.name == "verden":
                g = None
            date = datetime.fromtimestamp(row[3])
            d, created = Story.objects.get_or_create(parent=None, title=row[4].decode('utf-8'), user=u, updated=date, created=date, pub_date=date)
            d.content = text
            d.group = g
            d.save()
            self.make_children(cursor, row[0], d)
        conn.close()

    def make_children(self, db_cursor, debateid, debate):
        db_cursor.execute("select debateid, ownerid, groupid, created, title, contents, navn, brukernavn from debate inner join passord on passord.medlemid=ownerid inner join gruppe on gruppe.id = debate.groupid where parentid = %d" % (debateid,))
        for row in db_cursor.fetchall():
            did = row[0]
            u = User.objects.get(username=row[7].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[6].decode('utf-8').capitalize())
            if g.name == "verden":
                g = None
            date = datetime.fromtimestamp(row[3])
            dd, created = Story.objects.get_or_create(parent=debate, user=u, created=date, updated=date, pub_date=date)
            dd.title = title=row[4].decode('utf-8')
            dd.content = comment_converter(row[5])
            dd.group = g
            dd.save()
            self.make_children(db_cursor, did, dd)

