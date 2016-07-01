# read average weather data and generate realistic random weather
import random
import sys
import os
import re


class WeatherError(Exception):
    def __init__(self, value, info=""):
        self.value = value
        self.info = info

def read_wg_file(filenumber):
    file_path = "./weaterdata/weathergen"
    prefix = "r_"
    suffix = "_scen"
    extension = ".csv"
    file = file_path+prefix+filenumber+suffix+extension
    gw = 0
    text = open_file(file)
    data = read_file(text, gw)

def read_lw_file():
    file = choose_file_in_dir()
    text = open_file(file)
    td = TableDelimiters(cell_border=r"[\s]{2,}")
    lb = Labels(heading_row=5, unit_row=6)
    fw =FileSettings(delimiters=td, labels=lb)
    print(read_file(text, fw))


def choose_file_in_dir(directory="./weatherdata"):
    # Ask the user to select a file from the weatherdata directory
    try:
        files = os.listdir(directory)
    except OSError:
        raise WeatherError("NoDataDirectory")

    num_files = len(files)
    if num_files <= 0:
        raise WeatherError("NoDataFile")

    files.sort()
    print("Please chose a file from the following list (key in the item number): ", end=" ")

    for i in range(0, num_files):
        print("{}.{};".format(i + 1, files[i]), end="  ")
    print("")

    item = 1
    while True:
        try:
            item = int(sys.stdin.readline())
            if not (1 <= item <= num_files):
                print("The value you entered was not valid: please enter a number from 1 to {}".format(num_files))
            else:
                break
        except ValueError:
            print("The value you entered was not an integer: please try entering the item number again")

    filename = files[item - 1]
    print("Thank you - you have selected the data file:", filename)
    return directory + "/" + filename


def open_file(filename):
    try:
        data_file = open(filename, "r")
    except OSError:
        raise WeatherError("FileUnopenable")
    text = data_file.read()
    data_file.close()
    return text


# reads local weather(lw) from the met office
# these files have 5 lines of explanatory information
# followed by the column headings yyyy mm tmax tmin af rain sun
# followed by the units for each column blank blank degC degC days mm hours
# followed by the data, which may be marked with # or * in some cases, absent data marked ---

class TableDelimiters():
    def __init__(self,
                 cell_border=", ",
                 row_border="\n",
                 empty_cell="---",
                 ):
        # markers used to differentiate rows and cells
        self.cell_border = re.compile(cell_border)
        self.row_border = re.compile(row_border)
        self.empty_cell = re.compile(empty_cell)

class DataTypes():
    def __init__(self,
                 types="dt, it, ft, ft, it, ft, ft",
                 date_type=r"[0-9]{4}",
                 integer_type=r"[0-9]*",
                 float_type=r"-?[0-9]*\.[0-9]*",
                 ):
        # regex to check the data fits the expected types
        self.date_type = re.compile(date_type)
        self.short_type = re.compile(integer_type)
        self.float_type = re.compile(float_type)
        types = types.split(", ")
        self.types = []
        for x in types:
            if x == "dt":
                self.types.append(self.date_type)
            elif x == "it":
                self.types.append(self.short_type)
            elif x == "ft":
                self.types.append(self.float_type)
            else:
                self.types.append([])


class Labels():
    def __init__(self,
                 heading_row=None,
                 unit_row=None,
                 headings="yyyy, mm, tmax, tmin, af, rain, sun",
                 units = "degC, degC, days, mm, hours",
                 ):
        # rows containing useful labels
        self.heading_row = heading_row
        self.unit_row = unit_row
        self.headings = headings.split(", ")
        self.columns = len(self.headings)
        self.months_col = self.headings.index("mm")
        self.units = units.split(", ")
        self.labels = len(units)


class FileSettings:
    def __init__(self, delimiters=TableDelimiters(),
                 data_types=DataTypes(),
                 labels=Labels()):
        self.delimiters = delimiters
        self.data_types = data_types
        self.labels = labels



def read_file(text, filetype):
    delimiters = filetype.delimiters
    labels = filetype.labels
    text = remove_markers(text)
    data, rows = split_strip(text, delimiters)
    data, null_count, error_count = check_type(data, filetype, rows)
    data_monthly, error_count = trim_split_transpose(data, error_count, labels)
    report(null_count, error_count, labels)
    return data_monthly


def remove_markers(text):
    # remove markers
    markers = "*#"
    for char in markers:
        text = text.replace(char, "")
    return text


def split_strip(text, delimiters):
    # split the data into a 2D list and strip out whitespace
    text = text.strip()
    data = delimiters.row_border.split(text)
    rows = len(data)
    for i in range(rows):
        data[i] = data[i].strip()
        data[i] = delimiters.cell_border.split(data[i])
    return data, rows


def check_headings(data, labels):
    # check the headings and units meet our expectations
    if labels.heading_row and not data[labels.heading_row][:labels.columns] == labels.headings:
        raise WeatherError("WrongDataHeadings", data[labels.heading_row])
    if labels.unit_row and not data[labels.unit_row][:labels.labels] == labels.units:
        raise WeatherError("WrongDataUnits", data[labels.unit_row])


def check_type(data, filetype, rows):
    # check data and convert to appropriate variable type
    # record of unreadable and null data values

    datatypes = filetype.data_types
    delimiters = filetype.delimiters
    labels = filetype.labels

    null_count = [0] * labels.columns
    error_count = [0] * labels.columns

    for i in range(labels.unit_row + 1, rows):
        for j in range(labels.columns):
            if datatypes.types[j].match(data[i][j]) is None:
                if delimiters.empty_cell.match(data[i][j]):
                    null_count[j] += 1
                else:
                    error_count[j] += 1
                data[i][j] = None
            else:
                if datatypes.types[j] == datatypes.float_type:
                    data[i][j] = float(data[i][j])
                else:
                    data[i][j] = int(data[i][j])
    return data, null_count, error_count


def trim_split_transpose(data, error_count, labels):
    # trim away additional information
    del data[:labels.unit_row + 1]
    rows = len(data)
    for i in range(rows):
        data[i] = data[i][:labels.columns]

    # split data by month
    data_monthly = [[]] * 12
    for row in data:
        if 0 < row[labels.months_col] <= 12:
            data_monthly[row[labels.months_col] - 1].append(row)
        elif row[labels.months_col]:
            error_count[1] += 1

    # transpose columns to make analysis easier
    for i in range(12):
        data_monthly[i] = list(zip(*data_monthly[i]))
    return data_monthly, error_count


def report(null_count, error_count, labels):
    # announce success
    print("\nFile has been read successfully; any errors or empty cells are counted below:")
    print("Unreadable values by column:", end="")
    for i in range(labels.columns):
        print(labels.headings[i], "=", error_count[i], end="; ")
    print("\nEmpty cells by column:", end="")
    for i in range(labels.columns):
        print(labels.headings[i], "=", null_count[i], end="; ")
    print("\n")

try:
    read_lw_file()
except WeatherError as err:
    print(err.value, err.info)
print("done")
