from django.db import models
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from core.models import Common, Markdown, extend_markdown

class FlatPage(Common, Markdown):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    #enable_comments = models.BooleanField(_('enable comments'))
    #template_name = models.CharField(_('template name'), max_length=70, blank=True,
    #    help_text=_("Example: 'pages/contact_page.html'. If this isn't provided, the system will use 'pages/default.html'."))
    #registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site, related_name="pages")
    admingroup = models.ForeignKey(Group, related_name='administers_pages',
            verbose_name=_('writable for'))
    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
