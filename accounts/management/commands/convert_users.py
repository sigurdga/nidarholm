from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

import MySQLdb

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
                #import pdb; pdb.set_trace()
                self.stdout.write("%s\n" % (u,))
                u.email = row[2] or ""
                u.save()
        conn.close()
