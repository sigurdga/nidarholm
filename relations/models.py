from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _

class GroupCategory(models.Model):
    name = models.CharField(_('name'), max_length=40)

    class Meta:
        verbose_name = _('group category')
        verbose_name_plural = ('group categories')

    def __unicode__(self):
        return self.name

class GroupProfile(models.Model):
    name = models.CharField(_('name'), max_length=80)
    group = models.OneToOneField(Group, verbose_name=_('group'))
    groupcategory = models.ForeignKey(GroupCategory, verbose_name=_('group category'))
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)
    #permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True)

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __unicode__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(_('name'), max_length=80)
    groupprofile = models.ForeignKey(GroupProfile, verbose_name=_('group'))
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __unicode__(self):
        return self.name + " (" + self.groupprofile.name + ")"

class Membership(models.Model):
    group_profile = models.ForeignKey(GroupProfile, verbose_name=_('group'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    role = models.ForeignKey(Role, verbose_name=_('role'))

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')

    def __unicode__(self):
        return self.user.username + "-" + self.group_profile.name + "-" + self.role.name
