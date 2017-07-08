import os
from csvReader import csvReader as csv
from floss.settings import FEEDS_DIR

def read_feed_types():
    return read("types.csv", types_file())

def read_feeds():
    return read("feeds.csv", feed_file())

def types_file():
    """
    :return: a definition of the "feed types" file type of type FileSettings
    """
    types = csv.DataTypes(types=[0, 3, 3])
    lab = csv.Labels(
        headings="name, min, max",
        units=""
    )
    return csv.FileSettings(data_types=types, labels=lab)

def feed_file():
    types = csv.DataTypes(types=[0, 3, 3])
    lab = csv.Labels(
        headings="name, min, max",
        units=""
    )
    return csv.FileSettings(data_types=types, labels=lab)


def read(file_name, type):
    file = os.path.join(FEEDS_DIR, file_name)
    return csv.read_file(file, type)