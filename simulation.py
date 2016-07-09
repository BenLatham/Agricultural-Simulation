import weathergen
import maize
import forage
import dairy
import financials
import tests


def simulation(reps=1, year_0=3001, year_n=3030, start_month=1):
    crop_status, livestock_status, balance = initialise()
    for rep in range (reps):
        print(test, rep)
        day_counter = 0
        data = weathergen.read_wg_file(rep+1)
        for year in range(year_0, year_n):
            for i in range(12):
                month = (start_month + i) % 12
                month_end, crop_status = maize.monthly(day_counter, crop_status, data)
                forage.monthly(year, month)
                dairy.monthly(year, month)
                financials.monthly(year, month)
                day_counter = month_end
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
try:
    simulation()
except weathergen.WeatherError as err:
    print(err.value, err.info)
print("done")
