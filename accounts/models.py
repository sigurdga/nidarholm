from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from instruments.models import Instrument

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    #organization = models.ForeignKey(Organization)
    #verv m2m: kobles mot gruppe
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.SmallIntegerField(null=True, blank=True)
    #country: add later
    occupation = models.CharField(max_length=50, null=True, blank=True)
    employer = models.CharField(max_length=30, null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    joined = models.DateField(null=True, blank=True)
    # to be replaced by something generic, maybe use knowledge from other fields
    status = models.SmallIntegerField(null=True, blank=True)
    parent_organization_member_number = models.IntegerField(null=True, blank=True)
    insured = models.SmallIntegerField(null=True, blank=True)
    # to be replaced by something generic: organization added fields like instrument, verv
    account = models.IntegerField(null=True, blank=True) #reskontro
    instrument = models.ForeignKey(Instrument, null=True, blank=True)

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
