from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from core.models import Common

from markdown import markdown

def get_organization(request):
    host = request.get_host()
    return get_object_or_404(SiteProfile, site__domain=host)

class GroupCategory(models.Model):
    name = models.CharField(_('name'), max_length=40)
    slug = models.SlugField()

    class Meta:
        verbose_name = _('group category')
        verbose_name_plural = ('group categories')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('organization-group-category-detail', (), {'slug': self.slug})


class GroupProfile(models.Model):
    group = models.OneToOneField(Group, verbose_name=_('group'))
    email = models.EmailField(_('email'), null=True, blank=True)
    admin_email = models.EmailField(_('email to administrator'), null=True, blank=True)
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)
    groupcategory = models.ForeignKey(GroupCategory,
        null=True, blank=True, verbose_name=_('group category'))

    class Meta:
        verbose_name = _('group profile')
        verbose_name_plural = _('group profiles')
        ordering = ('number',)

    def __unicode__(self):
        return self.group.name

class Role(models.Model):
    name = models.CharField(_('name'), max_length=30)
    group = models.ForeignKey(Group, verbose_name=_('group'))
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __unicode__(self):
        return self.name + " (" + self.group.name + ")"


class Membership(models.Model):
    group = models.ForeignKey(Group, verbose_name=_('group'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    role = models.ForeignKey(Role, verbose_name=_('role'))

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')

    def __unicode__(self):
        return self.user.username + "-" + self.group.name + "-" + self.role.name


class SiteProfile(Common):
    site = models.OneToOneField(Site, verbose_name=_('site'))
    contact_text = models.TextField(_('page footer contact information'), null=True, blank=True, help_text=_('Use Markdown'))
    contact_html = models.TextField(null=True, blank=True)
    admingroup = models.ForeignKey(Group, related_name='administers_sites',
            verbose_name=_('administration group'))

    class Meta:
        verbose_name = _('site profile')
        verbose_name_plural = _('site profiles')

    def __unicode__(self):
        return self.site.name

    def save(self, *args, **kwargs):
        if self.contact_text:
            self.contact_html = markdown(self.contact_text)
        super(SiteProfile, self).save(*args, **kwargs)


def create_group_profile(sender, instance, created, **kwargs):
    if created:
        group_profile = GroupProfile()
        group_profile.group = instance
        group_profile.save()


def create_site_profile(sender, instance, created, **kwargs):
    if created:
        site_profile = SiteProfile()
        site_profile.site = instance
        site_profile.group = Group()
        site_profile.group.name = _('Members')
        site_profile.group.save()
        site_profile.admingroup = Group()
        site_profile.admingroup.name = _('Administrators')
        site_profile.admingroup.save()
        site_profile.save()


post_save.connect(create_group_profile, sender=Group)
post_save.connect(create_site_profile, sender=Site)
