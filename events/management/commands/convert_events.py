from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from events.models import Event, EventCategory

import MySQLdb
import time
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cursor.execute("select tittel, beskrivelse, sted, til, fra, s_time, e_time, brukernavn, navn, daginnslag, serie, viktighet from oppgave inner join passord on passord.medlemid = fra inner join gruppe on gruppe.id = til where mg='g'")
        for row in cursor.fetchall():
            self.stdout.write("%s\n" % (row[0],))
            u = User.objects.get(username=row[7].decode('utf-8'))
            g, created = Group.objects.get_or_create(name=row[8].decode('utf-8').capitalize())
            if g.name == "Verden":
                g = None
            start = row[5]
            if start:
                end = row[6]
                if not end:
                    end = None
                date = start + timedelta(weeks=-2)
                ec = None
                if row[11]:
                    ec, created = EventCategory.objects.get_or_create(title=str(row[11]), slug=str(row[11]))
                e, created = Event.objects.get_or_create(title=row[0].decode('utf-8'), user=u, updated=date, created=date, start=start, end=end)
                e.text = row[1].decode('utf-8')
                e.group = g
                e.event_serie = row[10]
                e.event_category = ec
                e.whole_day = row[9]
                e.save()
        conn.close()

