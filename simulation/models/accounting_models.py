import django.db.models as models
#from django.db import models
from .general_models import Scenario, Rep
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

MONTHS = (
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December")
)

##################### Data Loaded at the start of the simulation #####################
class ScenarioSpecificBase(models.Model):
    """Tables which have a unique name within each scenario"""
    scenario = models.ForeignKey(Scenario)
    name = models.CharField(max_length=20)

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        abstract=True
        unique_together=('scenario', 'name')


class Units(ScenarioSpecificBase):
    """table of the units of measure used in this database"""


class Goods(ScenarioSpecificBase):
    """holds descriptions of goods and services which may be transferred"""
    units = models.ForeignKey(Units)  # Units used to measure this item


class Prices(models.Model):
    item = models.OneToOneField(Goods, on_delete=models.CASCADE)
    price = models.FloatField()
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)


class Enterprises(ScenarioSpecificBase):
    """Divisions of the farm business"""
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)


class Accounts(ScenarioSpecificBase):
    opening_balance = models.FloatField(default=0)
    def __str__(self):
        return u'{0}'.format(self.id)

class AccountTypeBase(models.Model):
    type="Base"
    account = models.OneToOneField(
        Accounts,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return u'{0} - {1}'.format(self.type, self.account)

    class Meta:
        abstract = True

class AccountsCurrent(AccountTypeBase):
    type="Customer"
    overdraft_interest = models.FloatField(default=0)
    credit_interest = models.FloatField(default=0)
    overdraft_limit = models.FloatField(default=0)


class AccountsLoans(AccountTypeBase):
    type="Loan"
    interest =  models.FloatField(default=0)
    years_to_payback = models.FloatField(default=0)


class AccountsSupplier(AccountTypeBase):
    type="Supplier"
    credit_limit = models.FloatField(default=None, blank=True, null=True)
    interest = models.FloatField(default=0)
    max_delay = models.FloatField(default=0)  # length of time a payment can be defered in days


class AccountsCustomer(AccountTypeBase):
    type="Customer"
    payment_delay = models.FloatField(default=0)  # length of time before the debitor will withhold payment

class TradesSheet(models.Model):
    """Standard purchases and sales in any given month"""

    enterprise =models.ForeignKey(Enterprises)
    trader =models.ForeignKey(AccountsSupplier)
    item =models.ForeignKey(Goods)
    month =models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)], choices=MONTHS)
    quantity =models.FloatField()


##################### Data generated during each run #####################


class TransfersBase():
    """ Transactions in which goods of value are transfered"""
    date = models.DateField()
    item = models.ForeignKey(Goods)
    quantity = models.FloatField()
    unit_value = models.FloatField()
    rep = models.ForeignKey(Rep)

    class Meta:
        abstract = True

class InternalTransfers(TransfersBase):
    """ Transfers of goods within the farm business from enterprise to enterprise"""
    origin = models.ForeignKey(Enterprises,related_name="xfers_out")
    destination = models.ForeignKey(Enterprises,related_name="xfers_in")


class Sales(TransfersBase):
    """Transfers of goods from the farm to another party; these are linked to the debitor account of that party"""
    origin = models.ForeignKey(Enterprises)
    buyer = models.ForeignKey(AccountsCustomer)


class Purchases(TransfersBase):
    """Transfers of goods to the farm from another party; these are linked to the creditor account of that party"""
    vendor = models.ForeignKey(AccountsSupplier)
    destination = models.ForeignKey(Enterprises)


class Payments(models.Model):
    """Transfers of money between accounts"""
    rep = models.ForeignKey(Rep)
    date = models.DateField()
    origin = models.ForeignKey(Accounts, related_name="outgoing")
    destination = models.ForeignKey(Accounts, related_name="incoming")
    amount = models.FloatField()
