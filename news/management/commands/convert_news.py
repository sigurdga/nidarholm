from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from news.models import Story
from vault.models import UploadedFile
from django.conf import settings

import MySQLdb
import time
import re
import urllib2
import magic
import os
from os.path import basename
from datetime import datetime

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        img = re.compile(r'\<img.*?src=\/??(?:\'|\")([-:/%\ \w\.]*)')
        m = magic.open(magic.MAGIC_MIME)
        m.load()
        cursor.execute("select debateid, ownerid, groupid, created, title, contents, navn, brukernavn from debate inner join passord on passord.medlemid=debate.ownerid inner join gruppe on gruppe.id = debate.groupid where parentid = 155")
        for row in cursor.fetchall():
            #self.stdout.write("%s\n" % (row[4],))
            text = row[5].decode('utf-8')
            img_m = img.search(text)
            oid = None
            name = None
            if img_m:
                url = img_m.group(1)
                print url
                if not url.startswith("http"):
                    if url.startswith("/"):
                        url = "http://nidarholm.no" + url
                    else:
                        url = "http://nidarholm.no/" + url
                print url
                name = basename(url)
                try:
                    netfile = urllib2.urlopen(url)
                except urllib2.HTTPError:
                    print "Could not get: %s" % url
                else:
                    tmpcontents = netfile.read()
                    f, created = UploadedFile.objects.get_or_create(filename=name)
                    timestamp = datetime.now()
                    t = int(time.time())
                    f.uploaded = timestamp
                    short_folder = str(t)[-2:]
                    folder = settings.FILE_SERVE_ROOT + "originals/" + str(t)[-2:]
                    if not os.path.isdir(folder):
                        os.mkdir(folder)
                    path = folder + '/' + str(t)
                    short_path = short_folder + '/' + str(t)
                    f.file = short_path
                    outfile = open(path, "w")
                    outfile.write(tmpcontents)
                    outfile.close()
                    
                    f.content_type = m.file(path)
                    print f.content_type
                    f.save()
                    oid = f.id
                
            if oid:
            	text = re.sub(r'\<img.*?\>', '!['+name+']['+str(oid)+']', text)
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
            dd.content = row[5].decode('utf-8')
            dd.group = g
            dd.save()
            self.make_children(db_cursor, did, dd)

            

