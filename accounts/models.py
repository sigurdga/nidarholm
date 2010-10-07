from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    #organization = models.ForeignKey(Organization)
    #instrument m2m
    #verv m2m
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

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profiles.views.profile_detail', (), {'username': self.user.username})
