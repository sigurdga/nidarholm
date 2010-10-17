from django.db import models

class Instrument(models.Model):
    name = models.CharField(max_length=30)
    number = models.SmallIntegerField(db_index=True)

    def __unicode__(self):
        return self.name
