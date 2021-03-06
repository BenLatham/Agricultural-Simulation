# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 20:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0008_auto_20170828_2100'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Accounts',
            new_name='Account',
        ),
        migrations.RenameModel(
            old_name='AccountsCurrent',
            new_name='CurrentAccount',
        ),
        migrations.RenameModel(
            old_name='AccountsCustomer',
            new_name='CustomerAccount',
        ),
        migrations.RenameModel(
            old_name='Enterprises',
            new_name='Enterprise',
        ),
        migrations.RenameModel(
            old_name='Goods',
            new_name='Good',
        ),
        migrations.RenameModel(
            old_name='InternalTransfers',
            new_name='InternalTransfer',
        ),
        migrations.RenameModel(
            old_name='AccountsLoans',
            new_name='LoanAccount',
        ),
        migrations.RenameModel(
            old_name='Payments',
            new_name='Payment',
        ),
        migrations.RenameModel(
            old_name='Prices',
            new_name='Price',
        ),
        migrations.RenameModel(
            old_name='Purchases',
            new_name='Purchase',
        ),
        migrations.RenameModel(
            old_name='Sales',
            new_name='Sale',
        ),
        migrations.RenameModel(
            old_name='AccountsSupplier',
            new_name='SupplierAccount',
        ),
        migrations.RenameModel(
            old_name='TradesSheet',
            new_name='Trade',
        ),
        migrations.RenameModel(
            old_name='Units',
            new_name='Unit',
        ),
        migrations.AlterModelOptions(
            name='trade',
            options={'verbose_name_plural': 'TradesSheet'},
        ),
    ]
