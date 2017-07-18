from django.db import models
from .general_models import Scenario

class Feeds(models.Model):
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)
    me = models.FloatField()
    fme = models.FloatField()
    erdp = models.FloatField()
    dup = models.FloatField()
    qm = models.FloatField()
    feed_type = models.ForeignKey('FeedTypes', limit_choices_to={'scenario':scenario})
    maxInclusion = models.FloatField(null=True)

class FeedTypes(models.Model):
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)
    minInclusion = models.FloatField(null=True)
    maxInclusion = models.FloatField(null=True)