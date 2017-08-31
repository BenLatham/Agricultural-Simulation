from django.db import models
from django.contrib.auth.models import User

# table of the units of measure used in this database
class Scenario(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return u'{0} -({1})'.format(self.name, self.date)

class Rep(models.Model):
    scenario = models.ForeignKey(Scenario)
    number = models.IntegerField()
    class Meta:
        unique_together=('scenario', 'number')

class ScenarioSpecificBase(models.Model):
    """Tables which have a unique name within each scenario"""
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.scenario.name)

    class Meta:
        abstract=True
        unique_together=('scenario', 'name')