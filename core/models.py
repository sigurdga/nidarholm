from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from markdown import markdown

import re
from vault.models import UploadedFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

def extend_markdown(markdown_content):
    img_ids = [] # ids which will possibly get an automatic reference
    ref_ids = [] # ids of lines with references already
    for line in markdown_content.split():
        img_match = re.search(r'^\s*!\[.*?\]\[(\d+)\]', line)
        if img_match:
            img_ids.append(int(img_match.group(1)))
        ref_match = re.search(r'^\s*\[(\d+)\]:', line)
        if ref_match:
            ref_ids.append(int(ref_match.group(1)))
    for img_id in img_ids:
        if not img_id in ref_ids:
            ref_ids.append(img_id)
            try:
                img = UploadedFile.objects.get(id=img_id)
            except UploadedFile.DoesNotExist:
                pass
            else:
                markdown_content += "\n[{img_id}]: {img_url}".format(img_id=img_id, img_url=reverse('vault.views.send_file', kwargs={'id':img_id}))
    return markdown(markdown_content)


class TextEntry(models.Model):
    title = models.CharField(_('title'), max_length=60)
    slug = models.CharField(_('slug'), max_length=60)
    created = models.DateTimeField(_('created|datetime'), auto_now_add=True)
    updated = models.DateTimeField(_('updated|datetime'), auto_now=True)
    user = models.ForeignKey(User, verbose_name=_('created by|user'))
    group = models.ForeignKey(Group, verbose_name=_('created for|group'), null=True, blank=True)
    text = models.TextField(_('content'), blank=True, help_text=_('Use Markdown syntax'))
    text_html = models.TextField(_('html content'), blank=True)

    def save(self, *args, **kwargs):
        self.text_html = extend_markdown(self.text)
        self.slug = slugify(self.title)
        super(TextEntry, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['title']
