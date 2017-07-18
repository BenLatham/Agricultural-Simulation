import django.db.models as models
#from django.db import models
from .general_models import Scenario
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class ScenarioSpecificBase(models.Model):
    """Tables which have a unique name within each scenario"""
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)

    class Meta:
        abstract=True
        unique_together=('scenario', 'name')


class Units(ScenarioSpecificBase):
    """table of the units of measure used in this database"""


class Goods(ScenarioSpecificBase):
    """holds descriptions of goods and services which may be transferred"""
    units = models.ForeignKey(Units)  # Units used to measure this item


class Enterprises(ScenarioSpecificBase):
    """Divisions of the farm business"""
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)


class Accounts(ScenarioSpecificBase):
    opening_balance = models.FloatField(default=0)

class AccountTypeBase(models.Model):
    account = models.OneToOneField(
        Accounts,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        abstract = True

class AccountsCurrent(AccountTypeBase):
    overdraft_interest = models.FloatField(default=0)
    credit_interest = models.FloatField(default=0)
    overdraft_limit = models.FloatField(default=0)


class AccountsLoans(AccountTypeBase):
    interest =  models.FloatField(default=0)
    years_to_payback = models.FloatField(default=0)


class AccountsCreditor(AccountTypeBase):
    credit_limit = models.FloatField(default=None, blank=True, null=True)
    interest = models.FloatField(default=0)
    max_delay = models.FloatField(default=0)  # length of time a payment can be defered in days


class AccountsDebitor(AccountTypeBase):
    payment_delay = models.FloatField(default=0)  # length of time before the debitor will withhold payment


class TransfersBase():
    """ Transactions in which goods of value are transfered"""
    date = models.DateField()
    item = models.ForeignKey(Goods)
    quantity = models.FloatField()
    unit_value = models.FloatField()

    class Meta:
        abstract = True

class InternalTransfers(TransfersBase):
    """ Transfers of goods within the farm business from enterprise to enterprise"""
    origin = models.ForeignKey(Enterprises,related_name="xfers_out")
    destination = models.ForeignKey(Enterprises,related_name="xfers_in")


class Sales(TransfersBase):
    """Transfers of goods from the farm to another party; these are linked to the debitor account of that party"""
    origin = models.ForeignKey(Enterprises)
    buyer = models.ForeignKey(AccountsDebitor)


class Purchases(TransfersBase):
    """Transfers of goods to the farm from another party; these are linked to the creditor account of that party"""
    vendor = models.ForeignKey(AccountsCreditor)
    destination = models.ForeignKey(Enterprises)


class Payments(models.Model):
    """Transfers of money between accounts"""
    date = models.DateField()
    origin = models.ForeignKey(Accounts, related_name="outgoing")
    destination = models.ForeignKey(Accounts, related_name="incoming")
    amount = models.FloatField()


class PurchasesSheet(models.Model):
    """Standard purchases in any given month"""
    enterprise =models.ForeignKey(Enterprises)
    month =models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    quantity =models.FloatField()
    supplier =models.ForeignKey(AccountsCreditor)
    item =models.ForeignKey(Goods)


class SalesSheet(models.Model):
    """Standard sales in any given month"""
    enterprise =models.ForeignKey(Enterprises)
    month =models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    quantity =models.FloatField()
    buyer =models.ForeignKey(AccountsDebitor)
    item =models.ForeignKey(Goods)

class Prices(models.Model):
    item = models.OneToOneField(Goods, on_delete=models.CASCADE)
    price = models.FloatField()
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)