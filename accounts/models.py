from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    #organization = models.ForeignKey(Organization)
    #verv m2m: kobles mot gruppe
    cellphone = models.CharField(max_length=20, null=True, blank=True,
            verbose_name=_('cellphone'))
    address = models.CharField(max_length=50, null=True, blank=True,
            verbose_name=_('address'))
    postcode = models.SmallIntegerField(null=True, blank=True,
            verbose_name=_('postcode'))
    #country: add later
    occupation = models.CharField(max_length=50, null=True, blank=True,
            verbose_name=_('occupation'))
    employer = models.CharField(max_length=30, null=True, blank=True,
            verbose_name=_('employer'))
    born = models.DateField(null=True, blank=True,
            verbose_name=_('birth date'))
    joined = models.DateField(null=True, blank=True,
            verbose_name=_('joined date'))
    # to be replaced by something generic, maybe use knowledge from other fields
    status = models.SmallIntegerField(null=True, blank=True,
            verbose_name=_('membership status'))
    parent_organization_member_number = models.IntegerField(null=True, blank=True,
            verbose_name=_('external member number'))
    insured = models.SmallIntegerField(null=True, blank=True,
            verbose_name=_('insurance'))
    # to be replaced by something generic: organization added fields like instrument, verv
    account = models.IntegerField(null=True, blank=True,
            verbose_name=_('account reference')) #reskontro
    history = models.TextField(null=True, blank=True,
            verbose_name=_('membership history'))

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profiles.views.profile_detail', (), {'username': self.user.username})


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile()
        user_profile.user = instance
        user_profile.save()

post_save.connect(create_user_profile, sender=User)
