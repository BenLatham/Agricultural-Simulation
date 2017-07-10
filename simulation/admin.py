import csvReader.csvReader2 as csv

def load_costs():

    fields=[
        csv.Field("item","universal"),
        csv.Field("units","universal"),
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
    csv.CsvFile(
        fields=fields

    )

