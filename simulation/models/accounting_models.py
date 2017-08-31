import django.db.models as models
#from django.db import models
from .general_models import Scenario, Rep, ScenarioSpecificBase
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



class Unit(ScenarioSpecificBase):
    """table of the units of measure used in this database"""


class Good(ScenarioSpecificBase):
    """holds descriptions of goods and services which may be transferred"""
    units = models.ForeignKey(Unit)  # Units used to measure this item


class Price(models.Model):
    item = models.OneToOneField(Good, on_delete=models.CASCADE)
    price = models.FloatField()
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)


class Enterprise(ScenarioSpecificBase):
    """Divisions of the farm business"""
    start = models.DateField(default=None, blank=True, null=True)
    termination = models.DateField(default=None, blank=True, null=True)


class Account(ScenarioSpecificBase):
    opening_balance = models.FloatField(default=0)
    def __str__(self):
        account_type="Type Unknown"
        if hasattr(self,'currentaccount'):
            account_type = self.currentaccount._meta.verbose_name
        elif hasattr(self,'loanaccount'):
            account_type = self.loanaccount._meta.verbose_name
        elif hasattr(self,'customeraccount'):
            account_type = self.customeraccount._meta.verbose_name
        elif hasattr(self,'supplieraccount'):
            account_type = self.supplieraccount._meta.verbose_name
        return u'{0} ({1})'.format(self.id,account_type )

class AccountTypeBase(models.Model):
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return u'{0} - {1}'.format(self._meta.verbose_name, self.account)

    class Meta:
        abstract = True

class CurrentAccount(AccountTypeBase):
    overdraft_interest = models.FloatField(default=0)
    credit_interest = models.FloatField(default=0)
    overdraft_limit = models.FloatField(default=0)

    class Meta:
        verbose_name="Customer Account"
        verbose_name_plural = "Accounts-Current"


class LoanAccount(AccountTypeBase):
    interest =  models.FloatField(default=0)
    years_to_payback = models.FloatField(default=0)


    class Meta:
        verbose_name="Loan"
        verbose_name_plural = "Accounts-Loan"


class SupplierAccount(AccountTypeBase):
    credit_limit = models.FloatField(default=None, blank=True, null=True)
    interest = models.FloatField(default=0)
    max_delay = models.FloatField(default=0)  # length of time a payment can be defered in days

    class Meta:
        verbose_name="Supplier Account"
        verbose_name_plural = "Accounts-Supplier"



class CustomerAccount(AccountTypeBase):
    type="Customer"
    payment_delay = models.FloatField(default=0)  # length of time before the debitor will withhold payment

    class Meta:
        verbose_name="Customer Account"
        verbose_name_plural = "Accounts-Customer"

class Trade(models.Model):
    """Standard purchases and sales in any given month"""

    enterprise =models.ForeignKey(Enterprise)
    trader =models.ForeignKey(SupplierAccount)
    item =models.ForeignKey(Good)
    month =models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)], choices=MONTHS)
    quantity =models.FloatField()

    class Meta:
        verbose_name_plural = "TradesSheet"


##################### Data generated during each run #####################


class TransferBase(models.Model):
    """ Transactions in which goods of value are transfered"""
    date = models.DateField()
    item = models.ForeignKey(Good)
    quantity = models.FloatField()
    unit_value = models.FloatField()
    rep = models.ForeignKey(Rep)

    class Meta:
        abstract = True

class InternalTransfer(TransferBase):
    """ Transfers of goods within the farm business from enterprise to enterprise"""
    origin = models.ForeignKey(Enterprise, related_name="xfers_out")
    destination = models.ForeignKey(Enterprise, related_name="xfers_in")


class Sale(TransferBase):
    """Transfers of goods from the farm to another party; these are linked to the debitor account of that party"""
    origin = models.ForeignKey(Enterprise)
    buyer = models.ForeignKey(CustomerAccount)


class Purchase(TransferBase):
    """Transfers of goods to the farm from another party; these are linked to the creditor account of that party"""
    vendor = models.ForeignKey(SupplierAccount)
    destination = models.ForeignKey(Enterprise)


class Payment(models.Model):
    """Transfers of money between accounts"""
    rep = models.ForeignKey(Rep)
    date = models.DateField()
    origin = models.ForeignKey(Account, related_name="outgoing")
    destination = models.ForeignKey(Account, related_name="incoming")
    amount = models.FloatField()
