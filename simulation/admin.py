from django.contrib import admin

from . import models

admin.site.register(models.Unit)
admin.site.register(models.Good)
admin.site.register(models.Price)
admin.site.register(models.Enterprise)
admin.site.register(models.Account)
admin.site.register(models.CurrentAccount)
admin.site.register(models.LoanAccount)
admin.site.register(models.SupplierAccount)
admin.site.register(models.CustomerAccount)
admin.site.register(models.Trade)
admin.site.register(models.InternalTransfer)
admin.site.register(models.Sale)
admin.site.register(models.Purchase)
admin.site.register(models.Payment)
admin.site.register(models.Feed)
admin.site.register(models.FeedType)
admin.site.register(models.Scenario)
admin.site.register(models.Rep)
admin.site.register(models.Dataset)
admin.site.register(models.WeatherDay)