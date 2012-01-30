# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings

from urllib2 import urlopen
from Crypto.Cipher import AES
import base64
import subprocess

PADDING = '{'
BLOCK_SIZE = 32
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def trans(string):
    string = string.replace("æ","a")
    string = string.replace("ø","o")
    string = string.replace("å","a")
    string = string.replace(" ","")
    return string

class Command(BaseCommand):
    help = "Updates mailingslists based on group and organization membership"
    def handle(self, *args, **options):
        data = {'prefix': "nidarholm-", 'groups': ["Medlemmer", "Euph", "Klarinett", "Småmessing", "Fløyte", "Saksofon", "Horn", "Trombone", "Tuba", "Slagverk", "Obo", "Fagott"]}
        secret = settings.SECRET_KEY[0:16]
        cipher = AES.new(secret)

        encoded = EncodeAES(cipher, simplejson.dumps(data))

        host = settings.MAIN_HOST
        protocol = "http://"
        contents = urlopen(protocol + host + reverse('organization-email-lists', args=[encoded])).read()

        decoded = DecodeAES(cipher, contents)
        data = simplejson.loads(decoded)

        for listname,group in data.items():
            new_list = file("/tmp/" + listname, "w")
            for email in group:
                new_list.write(email + "\n")
            new_list.close()

            # next level
            command = '/usr/sbin/sync_members -f /tmp/' + listname + ' ' + listname
            process = subprocess.Popen(command.split(), shell=False, stdout=subprocess.PIPE)
            output = process.communicate()[0]
            if output:
                print "==================================="
                print group
                print output
