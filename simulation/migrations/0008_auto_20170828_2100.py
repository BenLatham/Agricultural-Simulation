# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-28 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulation', '0007_feeds_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalTransfers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.FloatField()),
                ('unit_value', models.FloatField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xfers_in', to='simulation.Enterprises')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Goods')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xfers_out', to='simulation.Enterprises')),
                ('rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Rep')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.FloatField()),
                ('unit_value', models.FloatField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Enterprises')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Goods')),
                ('rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Rep')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.AccountsSupplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('quantity', models.FloatField()),
                ('unit_value', models.FloatField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.AccountsCustomer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Goods')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Enterprises')),
                ('rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulation.Rep')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='feeds',
            unique_together=set([('scenario', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedtypes',
            unique_together=set([('scenario', 'name')]),
        ),
    ]
