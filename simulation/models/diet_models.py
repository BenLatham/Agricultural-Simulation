from django.db import models

class Feeds(models.Model):
    name = models.CharField(max_length=20)
    me = models.FloatField()
    fme = models.FloatField()
    erdp = models.FloatField()
    dup = models.FloatField()
    qm = models.FloatField()
    feed_type = models.ForeignKey('FeedTypes')
    maxInclusion = models.FloatField(null=True)

class FeedTypes(models.Model):
    name = models.CharField(max_length=20)
    minInclusion = models.FloatField(null=True)
    maxInclusion = models.FloatField(null=True)