from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

class ObjectPermission(models.Model):
    group = models.ForeignKey(Group)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
