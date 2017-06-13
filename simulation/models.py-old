from django.db import models


# Create your models here.
class SimulationYear(models.Model):
    year_ending = models.PositiveSmallIntegerField( default=1)

    def gross_margin (self):
        total = 0
        for enterprise in self.enterprise_set.all():
            total += enterprise.gross_margin()
        return total

    def __str__(self):
        return str(self.year_ending-1)+"-"+str(self.year_ending)


class Enterprise(models.Model):
    year = models.ForeignKey(SimulationYear, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="-")

    def total_income(self):
        return self.__sum(self.income_set.all())

    def total_xfers_out(self):
        return self.__sum(self.xferout_set.all())

    def total_costs(self):
        return self.__sum(self.costs_set.all())

    def total_xfers_in(self):
        return self.__sum(self.xferin_set.all())

    def __sum(self, query_set):
        total = 0
        for item in query_set:
            total += item.total()
        return total

    def gross_margin (self):
        return self.total_income()+self.total_xfers_out()-self.total_costs()-self.total_xfers_in()
    def __str__(self):
        return self.name

class ItemBase(models.Model):
    item = models.CharField(max_length=20, default="-")
    unit = models.CharField(max_length=20, default="-")
    unit_price = models.FloatField(default=0)
    no_units = models.FloatField("number of units", default=0)
    def total(self):
        return self.unit_price*self.no_units
    def __str__(self):
        return self.item
    class meta:
        abstract = True

class Income(ItemBase):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

class Cost(ItemBase):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

class Xfer(ItemBase):
    source_enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="xferout")
    destination_enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="xferin")

