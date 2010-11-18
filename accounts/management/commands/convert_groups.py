from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from relations.models import GroupCategory

import MySQLdb

class Command(BaseCommand):
    help = "Converts users not already converted, or updates their info"
    def handle(self, *args, **options):
        conn = MySQLdb.connect(host="localhost", user="nidarholmfiler", passwd="Si1iep3p", db="nidarholm")
        cursor = conn.cursor()
        cat, created = GroupCategory.objects.get_or_create(name='Instrumentgrupper')
        cursor.execute("select id, navn, moderator from gruppe where id>7 and id<28")
        for row in cursor.fetchall():
            self.stdout.write("%s\n" % (row[1],))
            if row[1]:
                g, created = Group.objects.get_or_create(name=row[1].decode('utf-8').capitalize())
                g.groupcategory = cat
                self.stdout.write("%s\n" % (g,))
                g.save()
	cursor.execute("select brukernavn, navn from medlem_av_gruppe inner join passord on passord.medlemid = medlem_av_gruppe.medlemid inner join gruppe on gruppeid = gruppe.id")
        for row in cursor.fetchall():
            self.stdout.write("put %s into %s\n" % (row[0], row[1]))
            g, created = Group.objects.get_or_create(name=row[1].decode('utf-8').capitalize())
            u = User.objects.get(username=row[0].decode('utf-8'))
            if u:
                u.groups.add(g)
            u.save()
        conn.close()
