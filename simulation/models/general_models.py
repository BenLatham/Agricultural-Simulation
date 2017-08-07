from django.db import models
from django.contrib.auth.models import User

# table of the units of measure used in this database
class Scenario(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)

class Rep(models.Model):
    scenario = models.ForeignKey(Scenario)
    number = models.IntegerField()
    class Meta:
        unique_together=('scenario', 'number')