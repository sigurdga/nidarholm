# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from django.conf import settings

from organization.models import SiteProfile
import subprocess

def trans(string):
    string = string.replace("æ","a")
    string = string.replace("ø","o")
    string = string.replace("å","a")
    string = string.replace(" ","")
    return string

class Command(BaseCommand):
    help = "Updates mailingslists based on group and organization membership"
    def handle(self, *args, **options):
        groups = ["Medlemmer", "Euph", "Klarinett", "Småmessing", "Fløyte", "Saksofon", "Horn", "Trombone", "Tuba", "Slagverk", "Obo", "Fagott"]
        organization_group = SiteProfile.objects.get(site__name="Musikkforeningen Nidarholm").group
        for group in groups:
            listname = "nidarholm-" + trans(group.lower())        
            new_list = file("/tmp/" + listname, "w")
            g = Group.objects.get(name=group)
            for user in g.user_set.all():
                if organization_group in user.groups.all():
                    if user.get_profile().status < 4 and user.email:
                        new_list.write(user.email + "\n")
            new_list.close()
            command = '/usr/sbin/sync_members -f /tmp/' + listname + ' ' + listname
            print command
            process = subprocess.Popen(command.split(), shell=False, stdout=subprocess.PIPE)
            output = process.communicate()[0]
            if output:
                print "==================================="
                print group
                print output
            #commands.getoutput("/usr/sbin/sync_members -f /tmp/" + listname)
