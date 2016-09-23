from django.contrib import admin

from .models import Enterprise, Income, SimulationYear


class IncomeInline(admin.TabularInline):
    model = Income
    extra = 1


class EnterpriseAdmin(admin.ModelAdmin):
    model = Enterprise
    inlines = [IncomeInline]

# Register your models here.
admin.site.register(SimulationYear)
admin.site.register(Enterprise, EnterpriseAdmin)
