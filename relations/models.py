from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

class GroupCategory(models.Model):
    name = models.CharField(_('name'), max_length=40)

    class Meta:
        verbose_name = _('group category')
        verbose_name_plural = ('group categories')

    def __unicode__(self):
        return self.name

class GroupProfile(models.Model):
    group = models.OneToOneField(Group, verbose_name=_('group'))
    email = models.EmailField(_('email'), null=True, blank=True)
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)
    groupcategory = models.ForeignKey(GroupCategory,
        null=True, blank=True, verbose_name=_('group category'))

    class Meta:
        verbose_name = _('group_profile')
        verbose_name_plural = _('group_profiles')

    def __unicode__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(_('name'), max_length=80)
    group = models.ForeignKey(Group, verbose_name=_('group'))
    number = models.SmallIntegerField(_('seaquence number'), null=True, blank=True)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __unicode__(self):
        return self.name + " (" + self.groupprofile.name + ")"

class Membership(models.Model):
    group = models.ForeignKey(Group, verbose_name=_('group'))
    user = models.ForeignKey(User, verbose_name=_('user'))
    role = models.ForeignKey(Role, verbose_name=_('role'))

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')

    def __unicode__(self):
        return self.user.username + "-" + self.group_profile.name + "-" + self.role.name



def create_group_profile(sender, instance, created, **kwargs):
    if created:
        group_profile = GroupProfile()
        group_profile.group = instance
        group_profile.save()

post_save.connect(create_group_profile, sender=Group)
