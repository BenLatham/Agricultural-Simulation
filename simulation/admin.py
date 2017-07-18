import csvReader.csvReader2 as csv
from floss.settings import COSTS_DIR
from simulation.models.accounting_models import Units, Goods, Enterprises
import os
from django.db import connection

class admin:
    scenario =None


    def setup(self):
        enterprises = ["fixed", "dairy", "maize", "forage"]
        enterprise_records = [Enterprises(scenario=self.scenario, name=enterprise) for enterprise in enterprises]
        self.save_all(enterprise_records)
        for enterprise in enterprises:
            self.load_costs(enterprise, enterprise+"_supplies.csv")


    def load_goods(self):
        data = self.read_goods_csv()
        unique_units = {record[1] for record in data}  # convert to a set so we exclude duplicates
        unit_records = [Units(scenario=self.scenario, unit=unit) for unit in unique_units]  # build the records
        self.save_all(unit_records)

        units_dict = self.get_all(Units)  # create a dict to look them up efficiently

        goods_records = [Goods(scenario=self.scenario, name=record[0], units=units_dict[record[1]]) for record in data]
        Goods.objects.bulk_create(goods_records)


    def read_goods_csv(self):
        """read the goods file from csv, and return an array of the data"""
        goods_file = os.path.join(COSTS_DIR, "goods.csv")
        fields = [
            csv.Field("good"),
            csv.Field("units")
        ]
        goods = csv.CsvFile(fields=fields, filepath=goods_file)
        goods.read_file()
        return goods.data


    def save_all(self, records):
        for record in records:
            record.full_clean()  # call full clean on each record
        Units.objects.bulk_create(records)  # save to the database


    def get_all(self, model):
        """

        :param model: a database model with fields scenario and name which are unique together
        :return:
        """
        records = model.objects.filter(scenario=self.scenario)
        {record.name: record for record in records}


    def load_costs(self, enterprise, file, year=None, ):
        fields = [
            csv.Field("item"),
            csv.Field("Jan", "float"),
            csv.Field("Feb", "float"),
            csv.Field("Mar", "float"),
            csv.Field("Apr", "float"),
            csv.Field("May", "float"),
            csv.Field("Jun", "float"),
            csv.Field("Jul", "float"),
            csv.Field("Aug", "float"),
            csv.Field("Sep", "float"),
            csv.Field("Oct", "float"),
            csv.Field("Nov", "float"),
            csv.Field("Dec", "float")
        ]
        costs = csv.CsvFile(fields=fields, filepath=file)



