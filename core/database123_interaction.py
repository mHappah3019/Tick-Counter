#from database_interaction import *

from datetime import datetime
import csv
import os
import pandas as pd

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")


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


def delete_type_count(instance_name, file): #TODO: test this shit
    instances = pd.read_csv(file, index_col=0, nrows=0).columns.tolist() #"Date" header is present too, so the list is not properly a list of only instances names
    f=pd.read_csv(file, dtype=str)
    
    keep_instancecs = instances.remove(instance_name)

    #basically a filter: we get a dataframe composed of only the data corresponding to the "headers" in keep_instances
    new_f = f[keep_instancecs]

    new_f.to_csv(file, index=False)


#https://stackoverflow.com/questions/46113078/pandas-add-value-at-specific-iloc-into-new-dataframe-column
def add_to_header(instance_name, file):
    df = pd.read_csv(file, dtype=str)
    rowIndex = df.index[0]
    df.loc[rowIndex, instance_name] = None
    df.to_csv(file, index=False)


def add_to_headers(instance_name):
    add_to_header(instance_name, "dailies.csv")
    add_to_header(instance_name, "weeklies.csv")
    add_to_header(instance_name, "monthlies.csv")


df = pd.read_csv("dailies.csv", dtype=str)
cacca = [i for i in list(range(0,15))]
df["instance_cacca"] = cacca

print(df)

def rename_type(old_name, new_name, file):
    df = pd.read_csv(file)
    df.rename(columns = {f'{old_name}':f'{new_name}'}, inplace = True)
    df.to_csv(file, index=False)


def rename_DATABASE(old_name, new_name):
    rename_type(old_name, new_name, "dailies.csv")
    rename_type(old_name, new_name, "weeklies.csv")
    rename_type(old_name, new_name, "monthlies.csv")
