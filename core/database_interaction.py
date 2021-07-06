import sys
import os

sys.path.append("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter") #TODO: fix this
#print(sys.path)

import database123_interaction as db_int
import utils.datetime_utils as dt_utils
import utils.general_utils as gen

from datetime import datetime
import csv
import pandas as pd
import sys
import os


TICK_INSTANCES = gen.find_data_abs_path("tick-instances.csv")
DAILIES = gen.find_data_abs_path("dailies.csv")
WEEKLIES = gen.find_data_abs_path("weeklies.csv")
MONTHLIES = gen.find_data_abs_path("monthlies.csv")


#tick-instances.csv keeps the logs for the last date the application was run on
#the date is in the last row, first column
def load_last_date(file):
    with open(TICK_INSTANCES, "r") as file:
        csv_reader = csv.reader(file)
        matrix = list(csv_reader)

        #print(matrix)

        last_date = matrix[-1][0]
        return last_date


#deletes corresponding row for the "instance_name" object
def delete_from_GUI(instance_name):
    df = pd.read_csv(TICK_INSTANCES, dtype=object)

    idx = get_row_index(instance_name, df)
    df.drop(df.index[idx], inplace=True)

    df.to_csv(TICK_INSTANCES, index=False)


#this functions works only for finding the index of the th-row in tick-instances.csv (return index of corresponding "Name" row)
def get_row_index(instance_name, df):
    return df.index[df["Name"] == instance_name].tolist()[0]


if __name__=="__main__":
    delete_from_GUI("xxx")

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

    if ( not dt_utils.is_same_date(current_date, last_saved_date) ):       #if current_date and last_saved_date are not actually the same date, then we shall set to zero the "Daily" count (in tick-instances.csv) of every instance
        db_int.save_daily_counts(last_saved_date)  # before resetting the daily counts, we shall save them in dailies.csv
        count_reset("day") #actually resetting the values
        
    if ( not dt_utils.is_sameweek_dates(current_date, last_saved_date) ):  #if current_date and last_saved_date are not in the same week, then we shall set to zero the "Weekly" count (in tick-instances.csv) of every instance
        db_int.save_weekly_counts(last_saved_date) # before resetting the weekly counts, we shall save them in weeklies.csv
        count_reset("week") #actually resetting the values
        
    if ( not dt_utils.is_samemonth_dates(current_date, last_saved_date) ): #if current_date and last_saved_date are not in the same month, then we shall set to zero the "Monthly" count (in tick-instances.csv) of every instance
        db_int.save_monthly_counts(last_saved_date) # before resetting the monthly counts, we shall save them in monthlies.csv
        count_reset("month") #actually resetting the values



def rename_GUI(old_name, new_name): 
    df = pd.read_csv(TICK_INSTANCES, dtype=object)
    idx = get_row_index(old_name, df)

    df.at[idx, "Name"] = new_name   #the selected element to be renamed is the one given by the intersection of "idx" index/row and "Name" column

    df.to_csv(TICK_INSTANCES, index=False)


def save_upon_closing(objects):
    with open(TICK_INSTANCES, "r") as file: 
                csv_file = csv.reader(file)
                matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                        #NB. numbers are converted into string values

                for i, instance in (enumerate(objects)):
                    print(f"tickframe {instance.name} updating")
                    daily_value = int(matrix[i+1][2]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                    matrix[i+1][2] = daily_value #actually updating the daily value
                    
                    weekly_value = int(matrix[i+1][3]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                    matrix[i+1][3] = weekly_value #actually updating the weekly value
                
                    monthly_value = int(matrix[i+1][4]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                    matrix[i+1][4] = monthly_value #actually updating the monthly value
                

    with open(TICK_INSTANCES, "w", newline="") as file1:
                csv_file1 = csv.writer(file1)
                csv_file1.writerows(matrix)