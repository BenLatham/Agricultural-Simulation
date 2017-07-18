from django.db import models
from .general_models import Scenario

# A set of data generated at one time
# consists of multiple runs so as to replicate the simulation
class Dataset(models.Model):
    scenario = models.ForeignKey(Scenario)
    #parent_dataset = models.CharField(max_length=20)
    #version = models.CharField(max_length=20)
    #emissions_scenario = models.CharField(max_length=20)
    benchmark_year = models.PositiveSmallIntegerField()
    #location = models.PositiveIntegerField()
    #spatial_average = models.CharField(max_length=20)
    #sampling_method = models.CharField(max_length=20)
    #temporal_frequency = models.CharField(max_length=20)

class WeatherDay(models.Model):
    dataset = models.ForeignKey(Dataset)
    run = models.PositiveIntegerField()
    year = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
    precipitation = models.FloatField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()
    mean_vapour_pressure = models.FloatField()
    mean_relative_humidity = models.FloatField()
    sunshine = models.FloatField()
    downward_diffuse_irradiation = models.FloatField()
    direct_irradiation = models.FloatField()
    potential_evapotranspiration = models.FloatField()
