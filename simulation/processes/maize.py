import functools
import math
test = "---"


def monthly(day_counter, crop_status, data):
    month = data["month"][day_counter]
    days = 0
    print(test,"Maize grows tall in %2d/%d" %(month, data["year"][day_counter]))
    function = functools.partial(planting)
    while data["month"][day_counter] == month:
        soil_temp(crop_status,data, day_counter)
        function(crop_status, data, day_counter)
        days += 1
        day_counter += 1
    return day_counter, crop_status


def planting(crop_status, data, day):
    print(test,"Looking for planting opportunity")


# Source: http://www.ntsg.umt.edu/sites/ntsg.umt.edu/files/c002p183.pdf
def soil_temp(crop_status, data, day):
    constants={"damping_factor":{"mineral":0.24, "organic":0.11},
               "constant_z":{"mineral":0.017, "organic":0.016},
               "lai_constant":{"mineral":0.15, "organic":0.15},
               "s1":{"mineral":0.95, "organic":0.95},
               "s2":{"mineral":0.40, "organic":0.40},
               "snow":{"mineral":0.20, "organic":0.20},
               "reference_lai":{"mineral":3.0, "organic":3.0}
               }
    soiltype ="mineral"
    soil = crop_status.soil
    yesterday_temp = soil.soil_temp
    depth = 0.1 # m
    leaf_area_index = 0
    damping_factor = constants["damping_factor"][soiltype]
    constant_z = constants["constant_z"][soiltype]
    lai_constant = constants["lai_constant"][soiltype]
    s1 = constants["s1"][soiltype]
    s2 =constants["s2"][soiltype]
    snow = constants["snow"][soiltype]
    reference_lai = constants["reference_lai"][soiltype]

    air_temp = (data["temp_dmin"][day]+data["temp_dmax"][day])/2

    if air_temp < 0:
        surf_temp = snow*air_temp
    else:
        surf_temp = air_temp(s1+(1-s1)*math.exp(-s2*(leaf_area_index-reference_lai)))

    soil.soil_temp = yesterday_temp + (surf_temp - yesterday_temp)*damping_factor * math.exp(-constant_z*depth) * math.exp(-lai_constant(leaf_area_index))


