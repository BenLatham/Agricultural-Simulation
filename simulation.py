import weathergen
import maize
import forage
import dairy
import financials
import tests

def simulation(reps=1, year_0=0, year_n=1, start_month=3):
    crop_status, livestock_status, balance = initialise()
    for rep in range (reps):
        weathergen.choose_file_in_dir()
        for year in range(year_0, year_n):
            for i in range(12):
                month = (start_month + i) % 12
                maize.monthly(year, month)
                forage.monthly(year, month)
                dairy.monthly(year, month)
                financials.monthly(year, month)
            financials.capital(year)

# 3. Generate starting balance sheets (conventional and non-financial)
def initialise():
    crop = (0, 0, 0)
    livestock = (0, 0, 0)
    financial = (0, 0, 0)
    return crop, livestock, financial

try:
    simulation()
except weathergen.WeatherError as err:
    print(err.value, err.info)
print("done")
