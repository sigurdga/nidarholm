from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from forum.models import Debate

import MySQLdb
import time
import re
from datetime import datetime

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        escaped_fnutts=re.compile(r'\\"')
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cursor.execute("select debateid, ownerid, groupid, created, title, contents, navn, brukernavn from debate inner join passord on passord.medlemid=debate.ownerid inner join gruppe on gruppe.id = debate.groupid where parentid = 1")
        for row in cursor.fetchall():
            self.stdout.write("%s\n" % (row[4],))
            u = User.objects.get(username=row[7].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[6].decode('utf-8').capitalize())
            if g.name == "Verden":
                g = None
            date = datetime.fromtimestamp(row[3])
            d, created = Debate.objects.get_or_create(parent=None, title=row[4].decode('utf-8'), user=u, updated=date, created=date)
            text = comment_converter(escaped_fnutts.sub('"', row[5]), u)
            d.text = text
            d.group = g
            d.save()
            self.make_children(cursor, row[0], d)
        conn.close()

    def make_children(self, db_cursor, debateid, debate):
        escaped_fnutts=re.compile(r'\\"')
        db_cursor.execute("select debateid, ownerid, groupid, created, title, contents, navn, brukernavn from debate inner join passord on passord.medlemid=ownerid inner join gruppe on gruppe.id = debate.groupid where parentid = %d" % (debateid,))
        for row in db_cursor.fetchall():
            did = row[0]
            u = User.objects.get(username=row[7].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[6].decode('utf-8').capitalize())
            if g.name == "Verden":
                g = None
            date = datetime.fromtimestamp(row[3])
            dd, created = Debate.objects.get_or_create(parent=debate, user=u, created=date, updated=date)
            dd.title = title=row[4].decode('utf-8')
            text = comment_converter(escaped_fnutts.sub('"', row[5]), u)
            dd.text = text
            dd.group = g
            dd.save()
            self.make_children(db_cursor, did, dd)

            

