def monthly(day_counter, crop_status, data):
    month = data["month"][day_counter]
    print("Maize grows tall in %2d/%d" %(month, data["year"][day_counter]))
    while data["month"][day_counter] == month:
        day_counter += 1
    return day_counter, crop_status
