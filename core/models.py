# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from markdown import markdown

from vault.models import UploadedFile
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.conf import settings

import re
import urllib2
import magic
import os

from os.path import basename
from datetime import datetime
from BeautifulSoup import BeautifulSoup


def slugify(value):
    """
    Normalizes a string using unidecode library. Lowercase it, remove
    punctuation and replace spacing with hyphens.

    >>> slugify(u'Blåbærsyltetøy')
    'Blabaersyltetoy'
    """
    from unidecode import unidecode
    from django.utils.safestring import mark_safe
    value = unidecode(value)
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return mark_safe(re.sub('[-\s]+', '-', value))

def replace_references(match_obj):
    # can the parsing be stricter, please?
    description = match_obj.group('description')
    path = match_obj.group('path')
    try:
        img_id, size = path.split('/')
        img_id = int(img_id)
    except ValueError:
        img_id = int(path)
        size = settings.DEFAULT_IMAGE_SIZE
    try:
        file_to_preview = UploadedFile.objects.get(id=img_id)
    except UploadedFile.DoesNotExist:
        return ""
    if file_to_preview.is_image():
        return """<div class="preview">
        <img src="%s" alt="%s"/>
        <p class="caption">%s</p></div>""" % (
            reverse('vault.views.send_file', kwargs={'id':img_id, 'size': size}),
            description,
            description,
            )
    else:
        return """<div class="preview">
        <h2>%s</h2>
        <p>Type: %s</p>
        <p class="caption">%s</p>
        <p><a href="%s">Last ned</a></p>
        <p><a href="%s">Informasjon</a></p>
        </div>""" % (
            file_to_preview.filename,
            file_to_preview.content_type,
            description,
            reverse('vault.views.send_file', kwargs={'id':img_id}),
            file_to_preview.get_absolute_url(),
            )


def extend_markdown(markdown_content):
    parsed = []
    pattern = re.compile(r'\!\[(?P<description>.*?)\]\[(?P<path>\d+(?:\/\d+)?)\]')
    for line in markdown_content.split('\n'):
        if line.find('![') > -1:
            a = pattern.sub(replace_references, line)
            parsed.append(a)
        else:
            parsed.append(line)

    return markdown('\n'.join(parsed))

def comment_converter(text):
    print text
    oid = None
    name = None
    soup = BeautifulSoup(text)
    m = magic.open(magic.MAGIC_MIME)
    m.load()

    for img in soup('img'):
        url = img['src'] 
        print url
        if not url.startswith("http"):
            if url.startswith("/"):
                url = "http://nidarholm.no" + url
            else:
                url = "http://nidarholm.no/" + url
        name = basename(url)
        try:
            netfile = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "Could not get: %s" % url
        else:
            tmpcontents = netfile.read()
            f, created = UploadedFile.objects.get_or_create(filename=name)
            timestamp = datetime.now()
            t = timestamp.strftime("%s%f")
            f.uploaded = timestamp
            short_folder = t[-2:]
            folder = settings.FILE_SERVE_ROOT + "originals/" + t[-2:]
            if not os.path.isdir(folder):
                os.mkdir(folder)
            path = folder + '/' + t
            short_path = short_folder + '/' + t
            f.file = short_path
            outfile = open(path, "w")
            outfile.write(tmpcontents)
            outfile.close()
            
            f.content_type = m.file(path)
            print f.content_type
            f.save()
            oid = f.id
        
        if oid:
            new_reference = '!['+name+']['+str(oid)+']'
            if img.parent.name == "a":
                img.parent.replaceWith(new_refence)
            else:
                img.replaceWith(new_refence)
    print unicode(soup)
    return unicode(soup)


class CommonManager(models.Manager):

    def for_user(self, user=None):
        if user and user.is_authenticated():
            return self.get_query_set().filter(Q(group=None) | Q(group__user=user))
        else:
            return self.get_query_set().filter(group=None)


class Common(models.Model):
    created = models.DateTimeField(_('created'))
    updated = models.DateTimeField(_('updated'))
    user = models.ForeignKey(User, verbose_name=_('created by'))
    group = models.ForeignKey(Group, verbose_name=_('created for'), null=True, blank=True)
    
    objects = CommonManager()

    class Meta:
        abstract = True


class Markdown(models.Model):
    content = models.TextField(_('content'), blank=True, null=True, help_text=_('Use Markdown syntax'))
    content_html = models.TextField(_('html content'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.content:
            self.content_html = extend_markdown(self.content)
        super(Markdown, self).save(*args, **kwargs)

    class Meta:
        abstract = True
 

class Title(models.Model):
    title = models.CharField(_('title'), max_length=60)
    slug = models.CharField(_('slug'), max_length=60)

    def save(self, *args, **kwargs):
        title = self.title
        slug = slugify(self.title)
        while self.__class__.objects.filter(slug=slug):
            title += "_"
            slug = slugify(title)
        self.slug = slug
        super(Title, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['title']
