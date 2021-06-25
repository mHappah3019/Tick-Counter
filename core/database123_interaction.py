import database_interaction
import utils.general_utils as gen

from datetime import datetime
import csv
import os
import sys
import pandas as pd


TICK_INSTANCES = gen.find_abs_path("tick-instances.csv")
DAILIES = gen.find_abs_path("dailies.csv")
WEEKLIES = gen.find_abs_path("weeklies.csv")
MONTHLIES = gen.find_abs_path("monthlies.csv")


def save_daily_counts(date):
    fields = [date]  #"date" comes from tick-instances1.csv

    with open(TICK_INSTANCES, "r") as f: #ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)      #skipping headers row
        for row in gen.skip_last(csv_reader):    #for every instance we want to store the daily count; plus we are skipping the last row of tick-instances
            fields.append(row[2]) #appending every instance's daily count, to be then appended to one single row, correspoding to "last_saved_date"
    
    with open(DAILIES, "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open(DAILIES, "a", newline='\n') as f1:
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
        for row in gen.skip_last(csv_reader):    #for every instance we want to store the weekly count; plus skipping last row
            fields.append(row[3]) #appending every instance's daily count, to be then appended to one single row, correspoding to the entire duration of the week
    
    with open(WEEKLIES, "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open(WEEKLIES, "a", newline='\n') as f1:
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
        for row in gen.skip_last(csv_reader):    #for every instance we want to store the monthly count; plus skipping last row
            fields.append(row[4]) #appending every instance's monthly count, to be then appended to one single row, correspoding to month name + year
    
    with open(MONTHLIES, "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open(MONTHLIES, "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #...checking if file ends with a newline (\n)
            f1.write("\n")                  #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [actual month, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just MONTHLY counts



def delete_counts(instance_name):
    delete_type_count(instance_name, "dailies.csv")     
    delete_type_count(instance_name, "weeklies.csv")
    delete_type_count(instance_name, "monthlies.csv")
    database_interaction.delete_from_GUI(instance_name, TICK_INSTANCES)


#function that deletes column corresponding to the instance_name for the corresponding file
#(can use for dailies.csv, weeklies.csv and monthlies.csv)
def delete_type_count(instance_name, file): #TODO: fix and test this shit
    instances = pd.read_csv(file, index_col=0, nrows=0).columns.tolist() #"Date" header is present too, so the list is not properly a list of only instances names
    f=pd.read_csv(file)
    
    keep_instances = instances.remove(instance_name)
    print("LIST:"+ file)
    print(instances)
    print(keep_instances)

    #basically a filter: we get a dataframe composed of only the data corresponding to the "headers" in keep_instances
    #new_f = f[keep_instances]

    #new_f.to_csv(file, index=False)

delete_type_count("Instance2", MONTHLIES)
print("\n\n\n\n\n")
delete_type_count("Instance1", DAILIES)


#https://stackoverflow.com/questions/46113078/pandas-add-value-at-specific-iloc-into-new-dataframe-column
def add_to_header(instance_name, file):
    df = pd.read_csv(file, dtype=object)
    rowIndex = df.index[0]
    df.loc[rowIndex, instance_name] = None
    df.to_csv(file, index=False)


#takes the instance name, and adds it as header to any "database" csv file
#in fact for all 3 "database" files every header corresponds to one instance
def add_to_headers(instance_name):
    add_to_header(instance_name, DAILIES)
    add_to_header(instance_name, WEEKLIES)
    add_to_header(instance_name, MONTHLIES)


def rename_type(old_name, new_name, file):
    df = pd.read_csv(file, dtype=object)
    df.rename(columns = {f'{old_name}':f'{new_name}'}, inplace = True)
    df.to_csv(file, index=False)


def rename_DATABASE(old_name, new_name):
    rename_type(old_name, new_name, DAILIES)
    rename_type(old_name, new_name, WEEKLIES)
    rename_type(old_name, new_name, MONTHLIES)

#rename_type("sosa", "sosa2", "dailies.csv")