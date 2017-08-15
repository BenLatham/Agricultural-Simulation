from django.db import models
from .general_models import Scenario

class Feeds(models.Model):
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)
    me = models.FloatField()
    fme = models.FloatField()
    erdp = models.FloatField()
    dup = models.FloatField()
    adf = models.FloatField()
    feed_type = models.ForeignKey('FeedTypes', limit_choices_to={'scenario':scenario})
    maxInclusion = models.FloatField(null=True)

    def qm_ruminant(self):
        """
        :return: ratio of metabolisable energy to gross energy
        """

class FeedTypes(models.Model):
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)
    minInclusion = models.FloatField(null=True)
    maxInclusion = models.FloatField(null=True)

class BreedDetails(models.Model):
    breed = models.CharField(max_length=20, unique=True)

    # Fox et. al. 1998
    MM = models.FloatField(null=True) # maintenance multiplier non-lactating
    MML = models.FloatField(null=True) # maintenance multiplier lactating
    BW = models.FloatField(null=True) # Calf Birth Weight kg
    peak_yield = models.FloatField(null=True) # Average peak milk yield kg
    BW_adjustment_Q1 = models.FloatField(null=True) # Q1 Birth weight adjustment/age of dam yr
    BW_adjustment_Q2 = models.FloatField(null=True) # Q2 Birth weight adjustment/age of dam yr
    BW_adjustment_Q3 = models.FloatField(null=True) # Q3 Birth weight adjustment/age of dam yr
    BW_adjustment_Q4 = models.FloatField(null=True) # Q4 Birth weight adjustment/age of dam yr







