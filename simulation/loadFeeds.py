import os
from csvReader import csvReader as csv
from floss.settings import BASE_DIR

def read_feed_types():
    file = os.path.join(BASE_DIR, "simulation", "feeds", "types.csv")
