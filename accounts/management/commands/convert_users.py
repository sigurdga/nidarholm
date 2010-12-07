from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from avatar.models import Avatar

from hashlib import md5
from datetime import datetime
import MySQLdb
import os

def udec(text):
    if text:
        return text.decode('utf-8')

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cursor.execute("select fornavn, etternavn, epost, brukernavn, passord, fodt, medlemnidarholm.innmeldt, nmfnummer, forsikrinstrument, historikk, reskontro, telefon, mobil, adresse, postnummer, webside, arbeidstittel, arbeidssted, arbeidsadresse, arbeidspostnummer, arbeidswebside, medlemintranett.innmeldt, innlogginger, sider, epostmelding, siste, medlem.id from medlem left outer join medlemnidarholm on medlem.id=medlemnidarholm.medlemid left outer join medlemsinfo on medlem.id = medlemsinfo.medlemid left outer join medlemintranett on medlem.id = medlemintranett.medlemid left outer join passord on medlem.id=passord.medlemid")
        for row in cursor.fetchall():
            self.stdout.write("%s\n" % (row[0],))
            if row[3]:
                u, created = User.objects.get_or_create(username=row[3].decode('utf-8'))
                u.first_name = row[0].decode('utf-8')
                u.last_name = row[1].decode('utf-8')
                self.stdout.write("%s\n" % (u,))
                u.email = row[2] or ""
                u.save()
                p = u.get_profile()
                p.cellphone = row[12]
                p.address = udec(row[13])
                p.postcode = row[14]
                p.personal_website = row[15]
                p.occupation = row[16]
                p.employer = row[17]
                p.employer_website = row[20]
                p.joined = row[6]
                if row[22]:
                    p.status = row[22]
                if row[23]:
                    date = datetime.fromtimestamp(row[23])
                    p.created = date
                    p.updated = date
                if row[7]:
                    p.parent_organization_member_number = row[7]
                p.insured = row[8]
                if row[10]:
                    p.account = row[10]
                p.history = udec(row[9])
                p.save()
                
                m = md5()
                m.update("s_%d" % (row[26]),)
                avatar_filename = m.hexdigest()
                print avatar_filename
                path = "/srv/www/nidarholm/website/webdocs/innhold/persongalleri/%s.jpg" % (avatar_filename,)
                copy_path = "%s%s%s" % (settings.MEDIA_ROOT, settings.AVATAR_STORAGE_DIR, u.username)
                if os.path.exists(path):
                    a, created = Avatar.objects.get_or_create(user=u, avatar=copy_path)
                    a.primary = True
                    a.save()

        conn.close()
