#from datetime_utils import *

from datetime import datetime
import csv
import pandas as pd
import sys
import os

sys.path.append("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")
os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")
print(sys.path)
print("gg")

from tests import datetime_utils

TICK_INSTANCES = "tick-instances.csv"

def skip_last(iterator):  #TODO: understand this
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def load_last_date(file):
    with open(file, "r") as file:
        csv_reader = csv.reader(file)
        matrix = list(csv_reader)

        #print(matrix)

        last_date = matrix[-1][0]
        return last_date


def delete_from_GUI(instance_name, file):
    df = pd.read_csv(file)

    idx = get_row_index(instance_name, df)
    df.drop(df.index[idx], inplace=True)

    df.to_csv(file, index=False)


def get_row_index(instance_name, df):
    return df.index[df["Name"] == instance_name].tolist()[0] #TODO: implementare gestione IndexError


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
        matrix[-1][0] = datetime.today().strftime("%d/%m/%Y") #modifichiamo la data in tick-instances1.csv

    with open(TICK_INSTANCES, "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix)


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


#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html
def rename_GUI(old_name, new_name): 
    df = pd.read_csv(TICK_INSTANCES)
    idx = get_row_index(old_name, df)

    df.at[idx, "Name"] = new_name

    df.to_csv(TICK_INSTANCES, index=False)
