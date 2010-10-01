from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from markdown import markdown

import re
from vault.models import UploadedFile
from django.core.urlresolvers import reverse
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
    return markdown_content
    

class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('HTML content'), blank=True)
    content_markdown = models.TextField(_('content'), blank=True, help_text=_('Use Markdown syntax'))
    pub_date = models.DateTimeField(_('Date published'), auto_now_add=True)
    #enable_comments = models.BooleanField(_('enable comments'))
    #template_name = models.CharField(_('template name'), max_length=70, blank=True,
    #    help_text=_("Example: 'pages/contact_page.html'. If this isn't provided, the system will use 'pages/default.html'."))
    #registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site, related_name="pages")

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def save(self):
        self.content = markdown(extend_markdown(self.content_markdown))
        super(FlatPage, self).save()
