from django.db import models
import csv

# table of the units of measure used in this database
class Units(models.Model):
    unit = models.CharField(max_length=20)

# holds descriptions of goods and services which may be transferred
class Goods(models.Model):
    name = models.CharField(max_length=20)
    # Units used to measure this item
    units = models.ForeignKey(Units)

class Accounts(models.Model):
    account_name = models.CharField(max_length=20)
    description = models.TextField()
    overdraft_interest = models.FloatField()
    credit_interest = models.FloatField()
    csv.reader()


class Enterprises(models.Model):
    enterprise_name = models.CharField(max_length=20)
    start = models.DateField()
    termination = models.DateField()


class Transactions(models.Model):
    item = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date = models.DateField()
    unit_value = models.FloatField()

    class Meta:
        abstract = True


class Transfers(Transactions):
    origin = models.ForeignKey(Enterprises, related_name="xfer_out")
    destination = models.ForeignKey(Enterprises, related_name="xfer_in")


class Sales(Transactions):
    origin = models.ForeignKey(Enterprises)
    destination = models.ForeignKey(Accounts)


class Purchases(Transactions):
    origin = models.ForeignKey(Accounts)
    destination = models.ForeignKey(Enterprises)