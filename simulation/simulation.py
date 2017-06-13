class Scenario():
    def __init__(self, reps, years, months):
        self.year=0
        self.reps =reps
        self.years=years
        self.months=months
        self.crops = Crop()
        self.forage = Forage()
        self.livestock = Livestock()
        self.financial = Financial()

    def run(self):
        for rep in range(self.reps):
            for year in range(self.years):
                for month in range(self.months):
                    weather = self.getWeather()
                    self.crops.newMonth(weather)
                    self.forage.newMonth(weather)
                    self.livestock.newMonth(weather)
                    self.livestock.financial()



    def getWeather(self):
        return 0

class Crop():
    def newMonth(self, weather):
        self.weather = weather

class Forage():
    def newMonth(self, weather):
        self.weather = weather

class Livestock():
    def newMonth(self, weather):
        self.weather = weather

class Financial():
    def newMonth(self):
        print("recalculating financial balances")
