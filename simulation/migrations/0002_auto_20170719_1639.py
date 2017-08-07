# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 15:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountsDebitor',
            new_name='AccountsCustomer',
        ),
        migrations.RenameModel(
            old_name='AccountsCreditor',
            new_name='AccountsSupplier',
        ),
        migrations.RenameModel(
            old_name='PurchasesSheet',
            new_name='TradesSheet',
        ),
        migrations.RemoveField(
            model_name='salessheet',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='salessheet',
            name='enterprise',
        ),
        migrations.RemoveField(
            model_name='salessheet',
            name='item',
        ),
        migrations.RenameField(
            model_name='tradessheet',
            old_name='supplier',
            new_name='trader',
        ),
        migrations.DeleteModel(
            name='SalesSheet',
        ),
    ]