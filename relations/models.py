from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


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
        return ('relations-group-category-detail', (), {'slug': self.slug})


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

    def __unicode__(self):
        return self.group.name


class Role(models.Model):
    name = models.CharField(_('name'), max_length=80)
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


class SiteProfile(models.Model):
    site = models.OneToOneField(Site, verbose_name=_('site'))
    primary_group = models.ForeignKey(Group,
            verbose_name=_('primary group'),
            related_name=_('site'))
    administration_group = models.ForeignKey(Group,
            verbose_name=_('administration group'),
            related_name=_('administers_site'))
    primary_groupcategory = models.ForeignKey(GroupCategory,
            verbose_name=_('primary group category'))

    def __unicode__(self):
        return self.site.name


def create_group_profile(sender, instance, created, **kwargs):
    if created:
        group_profile = GroupProfile()
        group_profile.group = instance
        group_profile.save()


def create_site_profile(sender, instance, created, **kwargs):
    if created:
        site_profile = SiteProfile()
        site_profile.site = instance
        site_profile.primary_group = Group()
        site_profile.primary_group.name = _('Members')
        site_profile.primary_group.save()
        site_profile.administration_group = Group()
        site_profile.administration_group.name = _('Administrators')
        site_profile.administration_group.save()
        site_profile.primary_groupcategory = Groupcategory()
        site_profile.primary_groupcategory.name = _('Activity groups')
        site_profile.primary_groupcategory.save()
        site_profile.save()


post_save.connect(create_group_profile, sender=Group)
post_save.connect(create_site_profile, sender=Site)
