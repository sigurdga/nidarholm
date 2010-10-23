from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from markdown import markdown

import re
from vault.models import UploadedFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.query_utils import Q
from django.conf import settings

def extend_markdown(markdown_content):
    img_ids = [] # ids which will possibly get an automatic reference
    ref_ids = [] # ids of lines with references already
    for line in markdown_content.split('\n'):
        img_match = re.search(r'\!\[.*?\]\[(\d+(?:\/\d+)?)\]', line)
        #import pdb; pdb.set_trace()
        if img_match:
            img_ids.append(img_match.group(1))
        ref_match = re.search(r'^\s*\[(\d+)\]:', line)
        if ref_match:
            ref_ids.append(int(ref_match.group(1)))
    for img_url in img_ids:
        try:
            img_id, size = img_url.split('/')
            img_id = int(img_id)
        except ValueError:
            img_id = int(img_url)
            size = settings.DEFAULT_IMAGE_SIZE
        if not img_id in ref_ids:
            ref_ids.append(img_id)
            try:
                img = UploadedFile.objects.get(id=img_id)
            except UploadedFile.DoesNotExist:
                pass
            else:
                markdown_content += "\n[{img_url}]: {url}".format(
                    img_url=img_url,
                    url=reverse('vault.views.send_file', kwargs={'id':img_id, 'size': size}))
    return markdown(markdown_content)

class CommonManager(models.Manager):

    def for_user(self, user=None):
        if user and user.is_authenticated():
            return self.get_query_set().filter(Q(group=None) | Q(group__user=user))
        else:
            return self.get_query_set().filter(group=None)

class TextEntry(models.Model):
    title = models.CharField(_('title'), max_length=60)
    slug = models.CharField(_('slug'), max_length=60)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('created by'))
    group = models.ForeignKey(Group, verbose_name=_('created for'), null=True, blank=True)
    text = models.TextField(_('content'), blank=True, help_text=_('Use Markdown syntax'))
    text_html = models.TextField(_('html content'), blank=True)

    objects = CommonManager()

    def save(self, *args, **kwargs):
        self.text_html = extend_markdown(self.text)
        self.slug = slugify(self.title)
        super(TextEntry, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['title']
