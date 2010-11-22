from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from tagging.models import Tag
from vault.models import UploadedFile

from datetime import datetime
import magic
import hashlib

import MySQLdb

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        m = magic.open(magic.MAGIC_MIME)
        m.load()
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cursor.execute("select filer.id, fra, filer.navn, filpeker, beskrivelse, gruppe, tid, katalog, brukernavn, gruppe.navn from filer inner join passord on passord.medlemid = fra inner join gruppe on gruppe.id=filer.gruppe order by tid desc")
        for row in cursor.fetchall():
            self.stdout.write("%s %s %s\n" % (row[3], row[8], row[9]))
            u = User.objects.get(username=row[8].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[9].decode('utf-8'))
            f, created = UploadedFile.objects.get_or_create(filename=row[3].decode('utf-8'))
            timestamp = datetime.fromtimestamp(float(row[6]))
            f.uploaded = timestamp
            original_filename = "/srv/www/nidarholm/website/webdocs/innhold/filer/%s.%s" % (hashlib.md5("f_%s" % (row[0],)).hexdigest(), row[2])
            folder = row[6][-2:]
            f.file = folder + '/' + row[6]
            #f.content_type = magic.Magic(mime=True).from_file(original_filename)
            f.content_type = m.file(original_filename)
            print original_filename
            print m.file(original_filename)
            f.tags = ",".join(self.find_tags(cursor, int(row[7])))
            if g.name == 'verden':
                g = None
            f.group = g
            f.user = u
            f.save()
        conn.close()

    def find_tags(self, db_cursor, folder_id):
        tags = []
        if folder_id:
            db_cursor.execute("select navn, mor, fra from filkatalog where id = %d" % (folder_id,))
            tag = None
            for row in db_cursor.fetchall():
                tag, created = Tag.objects.get_or_create(name=row[0].decode('utf-8'))
                if row[1]:
                    tags = self.find_tags(db_cursor, int(row[1]))
                tags.append(tag.name)
        return tags
