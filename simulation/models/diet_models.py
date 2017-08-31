from django.db import models
from .general_models import ScenarioSpecificBase
from django.forms.models import model_to_dict


class Feed(ScenarioSpecificBase):
    me = models.FloatField()
    fme = models.FloatField()
    erdp = models.FloatField()
    dup = models.FloatField()
    adf = models.FloatField()
    price = models.FloatField(null=True)
    avaliable = models.FloatField(null=True)

    feed_type = models.ForeignKey('FeedType')
    maxInclusion = models.FloatField(null=True)

    @property
    def qm_ruminant(self):
        """
        Yan+agnew 2004
        :return: ratio of metabolisable energy to gross energy
        """
        return (-0.000796 * self.adf) + 0.827

    aggregable = ["me", "fme", "erdp", "dup", "adf", "price", "qm_ruminant"]  # fields which can be meaningfully aggregated

    def to_dict(self):
        dict = model_to_dict(self)
        dict["feed_type"]=self.feed_type.id
        dict["qm_ruminant"]=self.qm_ruminant()
        return dict


class FeedType(ScenarioSpecificBase):
    minInclusion = models.FloatField(null=True)
    maxInclusion = models.FloatField(null=True)

    def to_dict(self):
        dict ={}
        dict["id"]=self.id
        dict["minInclusion"]=self.minInclusion
        dict["maxInclusion"]=self.maxInclusion
        return dict


# class BreedDetails(models.Model):
#     breed = models.CharField(max_length=20, unique=True)
#
#     # Fox et. al. 1998
#     MM = models.FloatField(null=True)  # maintenance multiplier non-lactating
#     MML = models.FloatField(null=True)  # maintenance multiplier lactating
#     BW = models.FloatField(null=True)  # Calf Birth Weight kg
#     peak_yield = models.FloatField(null=True)  # Average peak milk yield kg
#     BW_adjustment_Q1 = models.FloatField(null=True)  # Q1 Birth weight adjustment/age of dam yr
#     BW_adjustment_Q2 = models.FloatField(null=True)  # Q2 Birth weight adjustment/age of dam yr
#     BW_adjustment_Q3 = models.FloatField(null=True)  # Q3 Birth weight adjustment/age of dam yr
#     BW_adjustment_Q4 = models.FloatField(null=True)  # Q4 Birth weight adjustment/age of dam yr
