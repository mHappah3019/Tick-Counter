from datetime import datetime #https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime

import pandas as pd
import csv
import os

TICK_INSTANCES = "tick-instances.csv"

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

current_date = datetime.today()  #for now current_date can be thought as a global variable too

def skip_last(iterator):  #TODO: understand thiss
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def save_daily_counts(date):
    fields = [date]  #"date" comes from tick-instances1.csv

    with open(TICK_INSTANCES, "r") as f: #ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)      #skipping headers row
        for row in skip_last(csv_reader):    #for every instance we want to store the daily count; plus we are skipping the last row of tick-instances
            fields.append(row[2]) #appending every instance's daily count, to be then appended to one single row, correspoding to "last_saved_date"
    
    with open("dailies.csv", "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open("dailies.csv", "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #...checking if file ends with a newline (\n)
            f1.write("\n")                  #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [last_saved_date, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just DAILY counts


def save_weekly_counts(date):
    date_object = datetime.strptime(date, "%d/%m/%Y")    #takes "date" from tick-instances1.csv and converts it into datetime object
    
    week = date_object.isocalendar()[1]  #taking the week of this specific datetime object
    year = date_object.year              #taking the year of this specific datetime object
    start_of_week = datetime.fromisocalendar(year, week, 1).strftime("%d/%m/%Y")                     #based on the week and the year of the last saved date we can...
    end_of_week = datetime.fromisocalendar(year, week, 7).strftime("%d/%m/%Y")                       #...get monday and sunday for that specific week (start and end of the specific week)

    fields = [start_of_week + "-" + end_of_week] #formatting <start-of-week>-<end-of-week>

    with open(TICK_INSTANCES, "r") as f: #ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)      #skipping headers row
        for row in skip_last(csv_reader):    #for every instance we want to store the weekly count; plus skipping last row
            fields.append(row[3]) #appending every instance's daily count, to be then appended to one single row, correspoding to the entire duration of the week
    
    with open("weeklies.csv", "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open("weeklies.csv", "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #...checking if file ends with a newline (\n)
            f1.write("\n")                  #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [week, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts ar e just WEEKLY counts


def save_monthly_counts(date):
    date_object = datetime.strptime(date, "%d/%m/%Y") #takes "date" from tick-instances1.csv

    month_name = date_object.strftime("%B")  #We want to save months with their actual name, and not the number representing them
    year = str(date_object.year)             #taking the year

    fields = [month_name + " " + year] 

    with open(TICK_INSTANCES, "r") as f: #ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)      #skipping headers row
        for row in skip_last(csv_reader):    #for every instance we want to store the monthly count; plus skipping last row
            fields.append(row[4]) #appending every instance's monthly count, to be then appended to one single row, correspoding to month name + year
    
    with open("monthlies.csv", "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open("monthlies.csv", "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #...checking if file ends with a newline (\n)
            f1.write("\n")                  #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [actual month, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just MONTHLY counts


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
    

def check_count_reset():
    current_date = datetime.today()
    last_saved_date = load_last_date(TICK_INSTANCES) #taking this date from tick-instances1.csv

    if ( not is_same_date(current_date, last_saved_date) ):       #if current_date and last_saved_date are not actually the same date, then we shall set to zero the "Daily" count (in tick-instances.csv) of every instance
        save_daily_counts(last_saved_date)  # before resetting the daily counts, we shall save them in dailies.csv
        count_reset("day") #actually resetting the values
        
    if ( not is_sameweek_dates(current_date, last_saved_date) ):  #if current_date and last_saved_date are not in the same week, then we shall set to zero the "Weekly" count (in tick-instances.csv) of every instance
        save_weekly_counts(last_saved_date) # before resetting the weekly counts, we shall save them in weeklies.csv
        count_reset("week") #actually resetting the values
        
    if ( not is_samemonth_dates(current_date, last_saved_date) ): #if current_date and last_saved_date are not in the same month, then we shall set to zero the "Monthly" count (in tick-instances.csv) of every instance
        save_monthly_counts(last_saved_date) # before resetting the monthly counts, we shall save them in monthlies.csv
        count_reset("month") #actually resetting the values


def count_reset(info): 
    with open(TICK_INSTANCES, "r") as file:
        csv_file = csv.reader(file)
        matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                #NB. numbers are converted into string values
        if (info == "day"):
            option = 2
        elif (info == "week"):
            option = 3
        elif (info == "month"):
            option = 4

        #print(matrix)
        #print(len(matrix))

        for i in range(len(matrix) -2):
                matrix[i+1][option] = 0 #RESETTING...
        matrix[-1][0] = current_date.strftime("%d/%m/%Y") #modifichiamo la data in tick-instances1.csv

    with open(TICK_INSTANCES, "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix)
 

def load_last_date(file):
    with open(file, "r") as file:
        csv_reader = csv.reader(file)
        matrix = list(csv_reader)

        #print(matrix)

        last_date = matrix[-1][0]
        return last_date


# function that takes any date (datetime object)
# and truncates out of it any information we don't really care about for our comparisons
def trunc_datetime(someDate, option):
    if (option == "day"):
        return someDate.replace(hour=0, minute=0, second=0, microsecond=0)
    elif (option == "week"):                                                      
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif (option == "month"):
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


#current_date = datetime.today()
#check_count_reset()


def get_passed_ms():
    now = datetime.now()
    hours = now.hour
    minutes = hours*60 + now.minute
    seconds = minutes*60 + now.second
    return seconds*1000 #millisecondi

def get_remaining_ms():
    ms_in_aday = 86,400,000
    return ms_in_aday - get_passed_ms()


#this function gets called by the InstancesManager method delete_instance
#it takes instance_name from the InstanceManager attributes (self.instance.name):
#for dailies, weeklies, monthlies, we're referencing the deletion of the corrisponding column
#for tick-instances1, the deletion of the corresponding row
def delete_counts(instance_name):
    delete_type_count(instance_name, "dailies.csv")     
    delete_type_count(instance_name, "weeklies.csv")
    delete_type_count(instance_name, "monthlies.csv")
    delete_from_GUI(instance_name, TICK_INSTANCES)


def delete_type_count(instance_name, file): #TODO: test this shit
    instances = pd.read_csv(file, index_col=0, nrows=0).columns.tolist() #"Date" header is present too, so the list is not properly a list of only instances names
    f=pd.read_csv(file, dtype=str)
    
    keep_instancecs = instances.remove(instance_name)

    #basically a filter: we get a dataframe composed of only the data corresponding to the "headers" in keep_instances
    new_f = f[keep_instancecs]

    new_f.to_csv(file, index=False)


def delete_from_GUI(instance_name, file):
    df = pd.read_csv(file)

    idx = get_row_index(instance_name, df)
    df.drop(df.index[idx], inplace=True)

    df.to_csv(file, index=False)


def get_row_index(instance_name, df):
    return df.index[df["Name"] == instance_name].tolist()[0] #TODO: implementare gestione IndexError



#df = pd.read_csv("tick-instances1.csv")
#print(get_row_index("xxx", df))
#delete_from_GUI("ciccia33", "tick-instances1.csv")