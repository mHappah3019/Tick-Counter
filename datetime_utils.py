import datetime as datetime


# function that checks if 2 dates fall in the same week or not
# one is a datetime object, the other is a string formatted in a specific format
# returns True if the 2 dates fall in the same week
def is_sameweek_dates(date1_object, date2_string):               #"date<>_objects" stands for datetime object coming from the datetime module
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    
    week1 = date1_object.isocalendar()[1] # takes value 1 to 53 (number of the week of the year)
    week2 = date2_object.isocalendar()[1]

    dat1 = trunc_datetime(date1_object, "week") # makes month and year to be the only relevant "variables" for the later comparison
    dat2 = trunc_datetime(date2_object, "week")

    #checks both if the 2 dates have the same "week number" (1-53) and if they are in the same month of the same year
    return (week1 == week2) & (dat1==dat2)


# function that checks if 2 dates fall in the same month or not
# returns True if the 2 dates fall in the same month
def is_samemonth_dates(date1_object, date2_string):
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    dat1 = trunc_datetime(date1_object, "month")  # makes month and year to be the only relevant "variables" for the later comparison
    dat2 = trunc_datetime(date2_object, "month")

    return dat1 == dat2


# function that checks if 2 dates are actually the same date
def is_same_date(date1_object, date2_string):
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    dat1 = trunc_datetime(date1_object, "day")  # makes DAY, month and year to be the only relevant information for the later comparison
    dat2 = trunc_datetime(date2_object, "day")

    return dat1 == dat2
    

# function that takes any date (datetime object)
# and truncates out of it any information we don't really care about for our comparisons
def trunc_datetime(someDate, option):
    if (option == "day"):
        return someDate.replace(hour=0, minute=0, second=0, microsecond=0)
    elif (option == "week"):                                                      
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif (option == "month"):
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_passed_ms():
    now = datetime.now()
    hours = now.hour
    minutes = hours*60 + now.minute
    seconds = minutes*60 + now.second
    return seconds*1000 #millisecondi


def get_remaining_ms():
    ms_in_aday = 86,400,000
    return ms_in_aday - get_passed_ms()