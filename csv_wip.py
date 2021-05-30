#from datetime import date
from collections import deque
from datetime import datetime

import csv
import os

#TODO: valutare se mi conviene avere current_date come variabile globale

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

#TODO: takes the dates to be stored from somewhere, ideally from the second file I was thinking to implement (dailies.csv)
dates = deque(maxlen=2) # contains 2 dates
current_date = datetime.today()

def save_daily_counts():
    
    current_date = datetime.today().strftime("%d/%m/%Y") #getting current_date and formatting it
    fields = [current_date]

    with open("tick-instances.csv", "r") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:    #for every instance we want to store the daily count
            #TODO: https://stackoverflow.com/questions/14674275/skip-first-linefield-in-loop-using-csv-file
            fields.append(row[2]) #appending every instance daily count to be appended to one single row, correspoding to "current_date"
    with open("dailies.csv", "a") as f1:
        writer = csv.writer(f1)
        writer.writerow(fields)  #writing as row this corresponding list: [current_date, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just DAILY counts

# function that checks if 2 dates fall in the same week or not
# returns True if the 2 dates fall in the same week
def is_sameweek_dates(date1, date2): 
    dat1 = date1.isocalendar() # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = date2.isocalendar()
    return dat1[1] == dat2[1]

# function that checks if 2 dates fall in the same month or not
# returns True if the 2 dates fall in the same month
def is_samemonth_dates(date1, date2):
    dat1 = date1.isocalendar() # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = date2.isocalendar()
    return dat1[2] == dat2[2]


def is_same_date(date1, date2):
    return date1 == date2


#TODO: implementare "dates"
def save_date(today, dates):
    # prende in input un array con dates[0] == "ieri"
    # e dates[1] == vuoto

    # rende come output lo stesso array con dates[0] = "oggi"
    # e dates[1] == "vuoto"

    #appendo (ho ora quindi 2 elementi), e cancello la testa

    dates.append(today)
    dates.popleft()
    

def check_count_reset(dates):
    # TODO: gestire le prime esecuzioni di questa funzione, in quanto l'array "dates" sarà necessariamente vuoto
    current_date = datetime.today()
    if ( not is_same_date(current_date, dates[0]) ):
        save_date(current_date, dates)
        count_reset("day")
    elif ( not is_sameweek_dates(current_date, dates[0]) ):
        count_reset("week")
    elif( not is_samemonth_dates(current_date, dates[0]) ):
        count_reset("month")


def count_reset(info):

    with open("tick-instances.csv", "r") as file:
        csv_file = csv.reader(file)
        matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                #NB. numbers are converted into string values
        if (info == "day"):
            option = 2
        elif (info == "week"):
            option = 3
        elif (info == "month"):
            option = 4

        print(matrix)
        print(len(matrix))
        for i in range(len(matrix) -1):
                matrix[i+1][option] = 0 #RESETTING...

    with open("tick-instances1.csv", "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix)
 

#count_reset("week")
#count_reset("day")
#check_count_reset(dates)


def load_last_date():
    #TODO: capire da dove deve essere chiamata
    with open("dailies.csv", "r") as file:
        csv_reader = csv.reader(file)
        matrix = list(csv_reader)

        print(matrix)

        last_date = matrix[-1][0]
        dates.append(last_date)


load_last_date()
#print(dates)
    
