import os

from . import weathergen

from . import dairy
from . import financials
from . import forage
from . import maize
from . import admin
from . import models
from csvReader.csvReader import CsvReadError
import time


class Scenario():

    def __init__(self, user, datapath="default", reps=1):
        self.scenario = models.Scenario(user=user)
        self.scenario.full_clean()
        self.scenario.save()
        self.reps = reps
        admin.load_goods(self.scenario)
        print(test+"hi!")
        #for rep in range(1, self.reps+1):
            #print(test + "howdy!")
            #data = weathergen.read_wg_file(rep, datapath)
            #print(data.get("headings"))

    def run(self,  year_0=3001, year_n=3030, start_month=1):
        crop_status, livestock_status, balance = initialise()
        #time.sleep(2)
        for rep in range (self.reps):
            #print(test, rep)
            day_counter = 0
            #data = weathergen.read_wg_file(rep + 1)
            for year in range(year_0, year_n):
                for i in range(12):
                    month = (start_month + i) % 12
                    #month_end, crop_status = maize.monthly(day_counter, crop_status, data)
                    forage.monthly(year, month)
                    dairy.monthly(year, month)
                    financials.monthly(year, month)
                    #day_counter = month_end
                financials.capital(year)


class CropStatus():
    def __init__(self):
        self.age = 0
        self.growth_stage = -1
        self.OHU_acumulated = 0
        self.moisture = None
        self.adf  = None
        self.protein = None
        self.fme = None
        self.soil = SoilStatus(texture=[25,40,35])

class SoilStatus():
    def __init__(self, moisture=None, temp=None, n=None, p=None, k=None, texture=None):
        self.soil_moisture = moisture
        self.soil_temp = temp
        self.soil_N = n
        self.soil_P = p
        self.soil_K = k
        self.soil_texture = texture

# 3. Generate starting balance sheets (conventional and non-financial)
def initialise():
    crop = CropStatus()
    livestock = (0, 0, 0)
    financial = (0, 0, 0)
    return crop, livestock, financial

test = "---"
