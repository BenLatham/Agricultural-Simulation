import csvReader.csvReader2 as csv
from floss.settings import COSTS_DIR
from simulation.models.accounting_models import Units, Goods
import os


def load_goods():
    goods_file = os.path.join(COSTS_DIR,"goods.csv")
    fields=[
        csv.Field("good"),
        csv.Field("units")
    ]
    goods = csv.CsvFile(fields=fields, filepath=goods_file)
    goods.read_file()
    units ={record[1] for record in goods.data}

    return units


def load_costs(year):
    fixed_file=os.path.join(COSTS_DIR,"fixed.csv")
    dairy_file=os.path.join(COSTS_DIR,"var_dairy.csv")
    forage_file=os.path.join(COSTS_DIR, "var_forage.csv")
    maize_file=os.path.join(COSTS_DIR,"var_maize.csv")


    fields=[
        csv.Field("item"),
        csv.Field("Jan","float"),
        csv.Field("Feb","float"),
        csv.Field("Mar","float"),
        csv.Field("Apr","float"),
        csv.Field("May","float"),
        csv.Field("Jun","float"),
        csv.Field("Jul","float"),
        csv.Field("Aug","float"),
        csv.Field("Sep","float"),
        csv.Field("Oct","float"),
        csv.Field("Nov","float"),
        csv.Field("Dec","float")
    ]
    fixed = csv.CsvFile(fields=fields,filepath=fixed_file)
    dairy = csv.CsvFile(fields=fields,filepath=dairy_file)
    forage = csv.CsvFile(fields=fields,filepath=forage_file)
    maize = csv.CsvFile(fields=fields,filepath=maize_file)

if __name__ == '__main__':
    print(load_goods())


