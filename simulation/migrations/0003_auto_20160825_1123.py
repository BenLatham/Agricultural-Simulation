# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 10:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0002_auto_20160825_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enterprise',
            old_name='enterprise',
            new_name='name',
        ),
    ]